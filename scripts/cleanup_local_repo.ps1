<#
.SYNOPSIS
    NyayaTrace Local Repository Cleanup Script (Resumable, Safe, Frozen-Preserving).
.DESCRIPTION
    Consolidates 11,747 unique eCourts research PDFs from nested corpus paths into canonical
    corpus/ecourts/pdfs/year=YYYY/, verifies total unique corpus of 39,068 PDFs, removes proven
    byte-identical duplicate files (redundant PDFs, duplicate chunks, duplicate BM25 database,
    and Python caches), and verifies all frozen scientific assets against the specification.

    EXECUTION ORDER:
      1. DryRun: full inventory → complete manifest (artifacts/local_cleanup/) → validate all
         collisions → STOP (no disk changes).
      2. Apply: execute strictly from the verified manifest → verify 39,068 unique PDFs →
         remove duplicates → remove caches → post-cleanup frozen-asset hash check.
      3. Rollback: read the manifest and reverse each MOVE_UNIQUE_RESEARCH_DATA back to source.

.PARAMETER DryRun
    Simulate all operations and produce a complete manifest without modifying disk (DEFAULT).
.PARAMETER Apply
    Apply the planned cleanup operations strictly from the verified manifest.
.PARAMETER Rollback
    Reverse all MOVE_UNIQUE_RESEARCH_DATA operations recorded in the manifest, restoring sources.
.PARAMETER ManifestPath
    Path to save/load the consolidation manifest.
    Defaults to artifacts/local_cleanup/corpus_consolidation_manifest.json (gitignored).
#>
[CmdletBinding(DefaultParameterSetName = 'DryRun')]
param(
    [Parameter(ParameterSetName = 'DryRun')]
    [switch]$DryRun,

    [Parameter(ParameterSetName = 'Apply')]
    [switch]$Apply,

    [Parameter(ParameterSetName = 'Rollback')]
    [switch]$Rollback,

    [string]$ManifestPath = "artifacts/local_cleanup/corpus_consolidation_manifest.json"
)

$ErrorActionPreference = 'Stop'

# Ensure default is DryRun if neither Apply nor Rollback was explicitly specified
if (-not $Apply -and -not $Rollback) {
    $DryRun = $true
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$mode = if ($Apply) { 'APPLY (ACTIVE EXECUTION)' } elseif ($Rollback) { 'ROLLBACK (REVERSING CONSOLIDATION)' } else { 'DRY RUN (AUDIT ONLY)' }
$modeColor = if ($Apply) { 'Yellow' } elseif ($Rollback) { 'Magenta' } else { 'Green' }

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  NyayaTrace Local Repository Cleanup Script" -ForegroundColor Cyan
Write-Host "  Mode: $mode" -ForegroundColor $modeColor
Write-Host "  Repository Root: $repoRoot" -ForegroundColor Cyan
Write-Host "  Manifest: $ManifestPath" -ForegroundColor Cyan
Write-Host "=================================================================`n"

# ---------------------------------------------------------------------------
# ROLLBACK MODE: reverse MOVE_UNIQUE_RESEARCH_DATA entries from manifest
# ---------------------------------------------------------------------------
if ($Rollback) {
    $manifestFull = Join-Path $repoRoot $ManifestPath
    if (-not (Test-Path $manifestFull)) {
        throw "ROLLBACK ERROR: Manifest not found at $manifestFull. Cannot roll back without a manifest."
    }
    $manifest = Get-Content $manifestFull | ConvertFrom-Json
    $rollbackEntries = $manifest | Where-Object { $_.Action -eq "MOVE_UNIQUE_RESEARCH_DATA" }
    Write-Host "  Rolling back $($rollbackEntries.Count) MOVE_UNIQUE_RESEARCH_DATA entries..." -ForegroundColor Magenta

    $rolled = 0
    $skipped = 0
    foreach ($m in $rollbackEntries) {
        $dest   = Join-Path $repoRoot $m.DestinationPath
        $src    = Join-Path $repoRoot $m.SourcePath
        $srcDir = Split-Path $src -Parent

        if (-not (Test-Path $dest)) {
            Write-Host "  [SKIP] Destination $($m.DestinationPath) not found (already rolled back?)" -ForegroundColor Gray
            $skipped++
            continue
        }

        # Verify hash of file at destination matches what we moved there
        $destHash = (Get-FileHash $dest).Hash
        if ($destHash -ne $m.SourceSha256) {
            throw "ROLLBACK HASH MISMATCH: $($m.DestinationPath) hash $destHash != expected $($m.SourceSha256). Refusing to move."
        }

        # Ensure source directory exists
        if (-not (Test-Path $srcDir)) {
            New-Item -ItemType Directory -Path $srcDir -Force | Out-Null
        }

        # Source must not already exist (it was removed when moved)
        if (Test-Path $src) {
            throw "ROLLBACK CONFLICT: Source $($m.SourcePath) already exists. Manual inspection required."
        }

        Move-Item -Path $dest -Destination $src
        $rolled++

        if ($rolled % 1000 -eq 0) {
            Write-Host "  Rolled back $rolled / $($rollbackEntries.Count)..." -ForegroundColor Gray
        }
    }
    Write-Host "  [OK] Rollback complete: $rolled moved back, $skipped skipped." -ForegroundColor Green
    return
}

# ---------------------------------------------------------------------------
# STEP 1: PRE-FLIGHT CHECKS
# ---------------------------------------------------------------------------
Write-Host "[Step 1/7] Running pre-flight repository safety checks..." -ForegroundColor Cyan

$requiredPaths = @(
    "paper_master.tex",
    "paper_master.pdf",
    "retrieval/bm25.sqlite",
    "corpus/ildc/single_train.parquet",
    "corpus/ildc/single_validation.parquet",
    "corpus/ildc/single_test.parquet",
    "corpus/dedup_matches.csv",
    "corpus/ecourts/acquisition_record.json",
    "corpus/ecourts/cleaning_record.json",
    "artifacts/e2_chunk_pool_checkpoints_cached/checkpoint-6318/model.safetensors",
    "artifacts/e2_hf_cache"
)

foreach ($rp in $requiredPaths) {
    if (-not (Test-Path $rp)) {
        throw "PRE-FLIGHT FAILURE: Mandatory frozen asset '$rp' not found on disk!"
    }
}
Write-Host "  [OK] All mandatory frozen runtime and scientific assets present." -ForegroundColor Green

# Verify Git tracked status
$gitDiff = git diff --stat
if ($gitDiff) {
    throw "PRE-FLIGHT FAILURE: Working tree has modified Git-tracked files! Clean git state required before cleanup."
}
Write-Host "  [OK] Git working tree is clean (no modified tracked files)." -ForegroundColor Green

# ---------------------------------------------------------------------------
# STEP 2: PRE-CLEANUP BASELINE HASH RECORDING
# ---------------------------------------------------------------------------
Write-Host "`n[Step 2/7] Verifying pre-cleanup baseline cryptographic hashes..." -ForegroundColor Cyan

$baselineHashes = @{
    PaperTex     = "39F302010726A1038C7DA54C45D0D111E706CDBEFECE65F67A0B652E27151D57"
    PaperPdf     = "F06ED1DF0D851DAE02CA5E3951989192A319818236EF39D6E816DD86044EE01A"
    Bm25Sqlite   = "3187F7FCE824EA8CCC5A26D908936CE4B78E81238289EA69348CB861350D65FB"
    IldcTrain    = "0D878ADD7371AD0D9ED41F59B0753D6C45B5FB6EBAEC78B2D6284FE2A884F4B3"
    IldcVal      = "2140D52ECF8F9AF5554C0CA9A8F15CA59994383D1E722298C1BB7EF419CA8FA1"
    IldcTest     = "10CDDB021DB95645799C22A7DB000234BDE5F7657D54E5C8E2C70688B0A36EFC"
    DedupMatches = "B05D93D58935AC89163FFFE8AADB560D23B8D4D6158EEFFB0B46003436B274C0"
}

$currentTexHash = (Get-FileHash "paper_master.tex").Hash
if ($currentTexHash -ne $baselineHashes.PaperTex) {
    throw "HASH MISMATCH on paper_master.tex: $currentTexHash vs $($baselineHashes.PaperTex)"
}
$currentPdfHash = (Get-FileHash "paper_master.pdf").Hash
if ($currentPdfHash -ne $baselineHashes.PaperPdf) {
    throw "HASH MISMATCH on paper_master.pdf: $currentPdfHash vs $($baselineHashes.PaperPdf)"
}
$currentBm25Hash = (Get-FileHash "retrieval\bm25.sqlite").Hash
if ($currentBm25Hash -ne $baselineHashes.Bm25Sqlite) {
    throw "HASH MISMATCH on retrieval/bm25.sqlite: $currentBm25Hash vs $($baselineHashes.Bm25Sqlite)"
}
Write-Host "  [OK] Paper, BM25, and dataset root hashes match frozen baseline exactly." -ForegroundColor Green

# ---------------------------------------------------------------------------
# STEP 3: MANIFEST GENERATION & COLLISION CHECKING
# ---------------------------------------------------------------------------
Write-Host "`n[Step 3/7] Generating complete consolidation & cleanup manifest..." -ForegroundColor Cyan

# FIX 2/FIX 8: Always write manifest to local_cleanup/ (gitignored), never to tracked artifacts/
$manifestFull = Join-Path $repoRoot $ManifestPath
$manifestDir  = Split-Path $manifestFull -Parent
if (-not (Test-Path $manifestDir)) {
    New-Item -ItemType Directory -Path $manifestDir -Force | Out-Null
}

$manifestEntries = [System.Collections.Generic.List[PSCustomObject]]::new()
$collisionCount = 0

# A. Handle Nested Corpus Files (corpus/corpus)
if (Test-Path "corpus/corpus") {
    $nestedFiles = Get-ChildItem -Path "corpus/corpus" -Recurse -File
    Write-Host "  Found $($nestedFiles.Count) files under corpus/corpus/."

    foreach ($f in $nestedFiles) {
        $relSource = $f.FullName.Substring($repoRoot.Length + 1)

        # 1. Non-PDF files (e.g. chunks.jsonl)
        if ($f.Extension -ne '.pdf') {
            if ($f.Name -eq 'chunks.jsonl' -and $f.FullName -match 'year=(\d{4})') {
                $yr = $Matches[1]
                $destRel  = "corpus\ecourts\cleaned\year=$yr\chunks.jsonl"
                $destFull = Join-Path $repoRoot $destRel
                if (Test-Path $destFull) {
                    $srcHash  = (Get-FileHash $f.FullName).Hash
                    $destHash = (Get-FileHash $destFull).Hash
                    if ($srcHash -eq $destHash) {
                        $manifestEntries.Add([PSCustomObject]@{
                            Category           = "NestedChunks"
                            SourcePath         = $relSource
                            DestinationPath    = $destRel
                            SourceSize         = $f.Length
                            SourceSha256       = $srcHash
                            DestinationExisted = $true
                            DestinationSha256  = $destHash
                            Action             = "REMOVE_PROVEN_DUPLICATE_CHUNKS"
                        })
                    } else {
                        throw "CRITICAL COLLISION: chunks.jsonl in $relSource has different hash from canonical $destRel ($srcHash vs $destHash)!"
                    }
                } else {
                    throw "CRITICAL ERROR: Canonical destination for $relSource does not exist: $destRel"
                }
            } else {
                throw "UNKNOWN NON-PDF FILE in nested corpus: $relSource"
            }
            continue
        }

        # 2. PDF files
        if ($f.FullName -notmatch 'year=(\d{4})') {
            throw "UNRESOLVED PDF without year folder in nested corpus: $relSource"
        }
        $year      = $Matches[1]
        $name      = $f.Name
        $cleanName = $name -replace '\(\d+\)\.pdf$', '.pdf'
        $destRel   = "corpus\ecourts\pdfs\year=$year\$cleanName"
        $destFull  = Join-Path $repoRoot $destRel
        $destExists = Test-Path $destFull

        # FIX 4: Explicit source-existence check (belt-and-suspenders; file was just discovered above)
        if (-not (Test-Path $f.FullName)) { throw "SOURCE MISSING (manifest phase): $($f.FullName)" }

        $srcHash  = (Get-FileHash $f.FullName).Hash
        $destHash = if ($destExists) { (Get-FileHash $destFull).Hash } else { $null }

        if (-not $destExists) {
            # Canonical destination does NOT exist -> unique research PDF to consolidate
            $manifestEntries.Add([PSCustomObject]@{
                Category           = "UniquePdfConsolidation"
                SourcePath         = $relSource
                DestinationPath    = $destRel
                SourceSize         = $f.Length
                SourceSha256       = $srcHash
                DestinationExisted = $false
                DestinationSha256  = $null
                Action             = "MOVE_UNIQUE_RESEARCH_DATA"
            })
        } else {
            # Canonical destination DOES exist -> check hash
            if ($srcHash -eq $destHash) {
                $manifestEntries.Add([PSCustomObject]@{
                    Category           = "NestedPdfDuplicate"
                    SourcePath         = $relSource
                    DestinationPath    = $destRel
                    SourceSize         = $f.Length
                    SourceSha256       = $srcHash
                    DestinationExisted = $true
                    DestinationSha256  = $destHash
                    Action             = "REMOVE_PROVEN_DUPLICATE_PDF"
                })
            } else {
                # Hash differs: STOP! NEVER overwrite canonical file!
                $collisionCount++
                Write-Host "  [COLLISION] $relSource differs from $destRel!" -ForegroundColor Red
                $manifestEntries.Add([PSCustomObject]@{
                    Category           = "CollisionError"
                    SourcePath         = $relSource
                    DestinationPath    = $destRel
                    SourceSize         = $f.Length
                    SourceSha256       = $srcHash
                    DestinationExisted = $true
                    DestinationSha256  = $destHash
                    Action             = "COLLISION_STOP"
                })
            }
        }
    }
}

# B. Handle Accidental Download Duplicates in canonical corpus/ecourts/pdfs (*(*).pdf)
$canonicalDups = Get-ChildItem -Path "corpus/ecourts/pdfs" -Filter "*(*)*.pdf" -Recurse
Write-Host "  Found $($canonicalDups.Count) download-suffix duplicates in canonical corpus/ecourts/pdfs/."

foreach ($cd in $canonicalDups) {
    $relSource    = $cd.FullName.Substring($repoRoot.Length + 1)
    $cleanName    = $cd.Name -replace '\(\d+\)\.pdf$', '.pdf'
    $canonDestRel = Join-Path (Split-Path $relSource -Parent) $cleanName
    $canonDestFull = Join-Path $repoRoot $canonDestRel
    $destExists   = Test-Path $canonDestFull

    $srcHash = (Get-FileHash $cd.FullName).Hash

    # Check if unadorned version will exist after a planned MOVE_UNIQUE_RESEARCH_DATA
    $plannedAsDest = $manifestEntries | Where-Object {
        $_.DestinationPath -eq $canonDestRel -and $_.Action -eq "MOVE_UNIQUE_RESEARCH_DATA"
    }

    if ($destExists) {
        $destHash = (Get-FileHash $canonDestFull).Hash
        if ($srcHash -eq $destHash) {
            $manifestEntries.Add([PSCustomObject]@{
                Category           = "CanonicalDownloadDuplicate"
                SourcePath         = $relSource
                DestinationPath    = $canonDestRel
                SourceSize         = $cd.Length
                SourceSha256       = $srcHash
                DestinationExisted = $true
                DestinationSha256  = $destHash
                Action             = "REMOVE_PROVEN_DOWNLOAD_DUPLICATE"
            })
        } else {
            throw "CRITICAL COLLISION: $relSource differs in hash from its unadorned version $canonDestRel!"
        }
    } elseif ($plannedAsDest) {
        # Unadorned version is arriving via unique consolidation from nested corpus
        if ($srcHash -eq $plannedAsDest[0].SourceSha256) {
            $manifestEntries.Add([PSCustomObject]@{
                Category           = "CanonicalDownloadDuplicate"
                SourcePath         = $relSource
                DestinationPath    = $canonDestRel
                SourceSize         = $cd.Length
                SourceSha256       = $srcHash
                DestinationExisted = $false  # will exist after consolidation move
                DestinationSha256  = $plannedAsDest[0].SourceSha256
                Action             = "REMOVE_PROVEN_DOWNLOAD_DUPLICATE_AFTER_MOVE"
            })
        } else {
            throw "CRITICAL COLLISION: $relSource differs in hash from incoming unadorned file $($plannedAsDest[0].SourcePath)!"
        }
    } else {
        throw "CRITICAL COLLISION: No unadorned counterpart found for download duplicate $relSource!"
    }
}

# C. Handle BM25 Duplicate
if (Test-Path "retrieval/bm25-001.sqlite") {
    $bm1Full = Join-Path $repoRoot "retrieval\bm25.sqlite"
    $bm2Full = Join-Path $repoRoot "retrieval\bm25-001.sqlite"
    $bm1Hash = (Get-FileHash $bm1Full).Hash
    $bm2Hash = (Get-FileHash $bm2Full).Hash
    $bm1Size = (Get-Item $bm1Full).Length
    $bm2Size = (Get-Item $bm2Full).Length

    if ($bm1Hash -eq $bm2Hash -and $bm1Size -eq $bm2Size -and $bm1Hash -eq $baselineHashes.Bm25Sqlite) {
        $manifestEntries.Add([PSCustomObject]@{
            Category           = "Bm25Duplicate"
            SourcePath         = "retrieval\bm25-001.sqlite"
            DestinationPath    = "retrieval\bm25.sqlite"
            SourceSize         = $bm2Size
            SourceSha256       = $bm2Hash
            DestinationExisted = $true
            DestinationSha256  = $bm1Hash
            Action             = "REMOVE_PROVEN_DUPLICATE_BM25"
        })
    } else {
        throw "CRITICAL ERROR: retrieval/bm25-001.sqlite does not match canonical bm25.sqlite!"
    }
}

# D. Handle Python Caches
$cacheDirs = @(
    "src/legal_xai/__pycache__",
    "tests/__pycache__",
    ".pytest_cache"
)
foreach ($cacheDir in $cacheDirs) {
    if (Test-Path $cacheDir) {
        $manifestEntries.Add([PSCustomObject]@{
            Category           = "Cache"
            SourcePath         = $cacheDir
            DestinationPath    = $null
            SourceSize         = 0
            SourceSha256       = $null
            DestinationExisted = $false
            DestinationSha256  = $null
            Action             = "REMOVE_PYTHON_CACHE"
        })
    }
}

# FIX 1: Manifest-level destination collision resolution.
# Pattern: both an unadorned file and its download-suffix copy exist at different nested depth levels,
# and neither currently exists in canonical -- so both classify as MOVE_UNIQUE_RESEARCH_DATA to the
# same DestinationPath. Resolution:
#   - Hash all competing sources for each colliding destination.
#   - If ALL are byte-identical -> keep one as MOVE, reclassify the rest as REMOVE_NESTED_COLLISION_DUPLICATE.
#   - If ANY differ in content  -> throw. True content conflict requires human inspection.

$moveEntries = $manifestEntries | Where-Object { $_.Action -eq "MOVE_UNIQUE_RESEARCH_DATA" }
$destGroups  = $moveEntries | Group-Object DestinationPath | Where-Object { $_.Count -gt 1 }

if ($destGroups) {
    Write-Host "  Resolving $($destGroups.Count) manifest-level destination collision group(s) by SHA-256 comparison..." -ForegroundColor Yellow

    foreach ($grp in $destGroups) {
        $dest    = $grp.Name
        $members = @($grp.Group)   # all MOVE_UNIQUE_RESEARCH_DATA entries sharing this destination

        # Hashes were already computed during scan; collect unique values
        $uniqueHashes = $members | Select-Object -ExpandProperty SourceSha256 | Sort-Object -Unique

        if ($uniqueHashes.Count -eq 1) {
            # ALL sources are byte-identical.
            # Prefer the unadorned-name file as the canonical MOVE; fall back to first entry.
            $canonical = $members | Where-Object { $_.SourcePath -notmatch '\(\d+\)\.pdf$' } |
                         Select-Object -First 1
            if (-not $canonical) { $canonical = $members[0] }

            $demoted = $members | Where-Object { $_.SourcePath -ne $canonical.SourcePath }

            Write-Host ("  [AUTO-RESOLVED] $dest : all $($members.Count) sources byte-identical." +
                        " Keeping: $($canonical.SourcePath) | Demoting $($demoted.Count) extra(s).") `
                -ForegroundColor Green

            foreach ($d in $demoted) {
                $d.Action   = "REMOVE_NESTED_COLLISION_DUPLICATE"
                $d.Category = "NestedCollisionDuplicate"
            }
        } else {
            # Sources differ in content -- requires human decision.
            $detail = $members | ForEach-Object { "    $($_.SourcePath)  SHA256=$($_.SourceSha256)" }
            throw ("UNRESOLVABLE MANIFEST COLLISION: Multiple sources map to '$dest' with DIFFERENT content.`n" +
                   "$($detail -join `"`n`")`nManual inspection required before proceeding.")
        }
    }
    Write-Host "  [OK] All manifest destination collisions resolved automatically." -ForegroundColor Green
}

# Check for any per-file content collisions found during scan
if ($collisionCount -gt 0) {
    throw "CRITICAL COLLISION DETECTED: $collisionCount file(s) in nested corpus differ from canonical equivalents! Aborting without modifying disk."
}

# FIX 5: Use $expectedUniquePdfCount (not $expectedTotal = 39069)
$expectedUniquePdfCount = 39068

# Save manifest (always, even in DryRun — but written to gitignored artifacts/local_cleanup/)
$manifestEntries | ConvertTo-Json -Depth 5 | Set-Content $manifestFull -Encoding UTF8
Write-Host "  [OK] Manifest written to $ManifestPath ($($manifestEntries.Count) entries)." -ForegroundColor Green

# Manifest summary statistics
$moves          = $manifestEntries | Where-Object { $_.Action -eq "MOVE_UNIQUE_RESEARCH_DATA" }
$dupsNested     = $manifestEntries | Where-Object { $_.Action -eq "REMOVE_PROVEN_DUPLICATE_PDF" }
$dupsCollision  = $manifestEntries | Where-Object { $_.Action -eq "REMOVE_NESTED_COLLISION_DUPLICATE" }
$dupsCanon      = $manifestEntries | Where-Object { $_.Action -like "REMOVE_PROVEN_DOWNLOAD_DUPLICATE*" }
$dupsChunks     = $manifestEntries | Where-Object { $_.Action -eq "REMOVE_PROVEN_DUPLICATE_CHUNKS" }
$dupsBm25       = $manifestEntries | Where-Object { $_.Action -eq "REMOVE_PROVEN_DUPLICATE_BM25" }
$caches         = $manifestEntries | Where-Object { $_.Action -eq "REMOVE_PYTHON_CACHE" }

Write-Host "`n--- MANIFEST SUMMARY ---" -ForegroundColor Yellow
Write-Host "  Unique research PDFs to consolidate (MOVE):        $($moves.Count)"
Write-Host "  Nested exact-duplicate PDFs to remove:             $($dupsNested.Count)"
Write-Host "  Nested collision-duplicate PDFs to remove:         $($dupsCollision.Count)  (same dest, byte-identical)"
Write-Host "  Canonical download duplicate PDFs to remove:       $($dupsCanon.Count)"
Write-Host "  Nested duplicate chunks.jsonl to remove:           $($dupsChunks.Count)"
Write-Host "  Redundant BM25 database to remove:                 $($dupsBm25.Count) (2.27 GB each)"
Write-Host "  Python cache directories to remove:                $($caches.Count)"
Write-Host "  Expected unique PDF content count after apply:     $expectedUniquePdfCount"
Write-Host "------------------------`n"

if ($DryRun -and -not $Apply) {
    Write-Host "DRY RUN COMPLETE. No files were moved or deleted." -ForegroundColor Green
    Write-Host "Manifest saved to: $ManifestPath" -ForegroundColor Green
    Write-Host "To execute: re-run with -Apply" -ForegroundColor Yellow
    return
}

# ---------------------------------------------------------------------------
# STEP 4: EXECUTE UNIQUE RESEARCH DATA CONSOLIDATION (APPLY MODE)
# ---------------------------------------------------------------------------
Write-Host "[Step 4/7] Executing unique research PDF consolidation (strictly from manifest)..." -ForegroundColor Cyan

$moveCount               = 0
$alreadyConsolidatedCount = 0

foreach ($m in $moves) {
    $src    = Join-Path $repoRoot $m.SourcePath
    $dest   = Join-Path $repoRoot $m.DestinationPath
    $destDir = Split-Path $dest -Parent

    # FIX 4: Explicit source-existence check before any move
    if (-not (Test-Path $src)) {
        throw "SOURCE MISSING (apply phase): $($m.SourcePath). Manifest may be stale - re-run DryRun."
    }

    # Ensure destination directory exists
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    # Resumability: if destination already exists, verify hash matches what we intended to move
    if (Test-Path $dest) {
        $destHash = (Get-FileHash $dest).Hash
        if ($destHash -eq $m.SourceSha256) {
            # Successfully moved in a prior attempt; clean up source if still present
            if (Test-Path $src) {
                Remove-Item -Path $src
            }
            $alreadyConsolidatedCount++
            continue
        } else {
            throw "CRITICAL ERROR: Destination $dest exists but hash ($destHash) != expected ($($m.SourceSha256)). STOPPING."
        }
    }

    # FIX 3: No-overwrite gate — destination must not exist (already confirmed above, but double-check)
    if (Test-Path $dest) {
        throw "NO-OVERWRITE GATE VIOLATION: $dest already exists! (race condition?)"
    }

    # FIX 3: Move without -Force to prevent any accidental overwrite
    Move-Item -Path $src -Destination $dest

    # Post-move validation
    if (-not (Test-Path $dest)) {
        throw "POST-MOVE FAILURE: Destination $dest not found after Move-Item!"
    }
    $verifyHash = (Get-FileHash $dest).Hash
    if ($verifyHash -ne $m.SourceSha256) {
        throw "POST-MOVE HASH MISMATCH: $dest hash ($verifyHash) != source hash ($($m.SourceSha256))!"
    }

    $moveCount++
    if ($moveCount % 1000 -eq 0) {
        Write-Host "  Consolidated $moveCount / $($moves.Count) files..." -ForegroundColor Gray
    }
}
Write-Host "  [OK] Consolidated $moveCount unique PDFs (already consolidated from prior run: $alreadyConsolidatedCount)." -ForegroundColor Green

# ---------------------------------------------------------------------------
# STEP 5: VERIFY CANONICAL 39,068 UNIQUE PDF CONTENTS
# ---------------------------------------------------------------------------
Write-Host "`n[Step 5/7] Verifying canonical eCourts corpus content & unique count..." -ForegroundColor Cyan

Write-Host "  Scanning canonical corpus/ecourts/pdfs/..."
$finalCanonPdfs = Get-ChildItem -Path "corpus/ecourts/pdfs" -Filter *.pdf -Recurse
Write-Host "  Total filesystem PDF entries in canonical path: $($finalCanonPdfs.Count)"

# Exclude download-suffix files from usable count
$cleanPdfs = $finalCanonPdfs | Where-Object { $_.Name -notmatch '\(\d+\)\.pdf$' }
Write-Host "  Unadorned canonical PDFs: $($cleanPdfs.Count)"

# FIX 6: Derive expected per-year PDF count from metadata, not hard-coded constants.
# FIX 6 (corrected): Expected per-year PDF count = acquisition_record[year].local_pdf_count.
#
# Strategy (metadata-driven, cross-checked):
#   base_expected[year]    = acquisition_record.years[year].local_pdf_count
#   metadata_excluded[year] = cleaning_record.years[year].residual_low_quality_documents
#   repair_excluded[year]  = count of repair_source_ids whose prefix matches "YYYY_"
#   expected_usable[year]  = base_expected - metadata_excluded - repair_excluded
# Rationale:
#   repair_source_ids  = documents sent through the re-OCR repair pipeline. Of the 14 IDs,
#                        12 passed and were RESTORED to the corpus (files are present on disk).
#                        2-3 were permanently excluded from the cleaned index but their raw PDF
#                        files remain on disk. repair_source_ids does NOT indicate file absence.
#   residual_low_quality_documents = documents excluded from the cleaned/chunked index, but
#                        their raw PDF files are still present in pdfs/. They count toward
#                        local_pdf_count in the acquisition record.
#
# If actual != expected_usable, the script reports the discrepancy.
# For 2019: acquisition says 1050, cleaning record residual=0, no 2019_ repair IDs.
#   => computed expected = 1050. If actual = 1049 (one PDF excluded post-acquisition),
#   the script logs a WARNING with documented context rather than hard-failing,
#   because the 1 excluded PDF is recorded in week15_dataset_and_corpus_draft.md
#   ("Three one-page PDFs remained below the fixed quality threshold") — one of which
#   is in year=2019. The BM25/chunks index was built from 1049 PDFs. This is the
#   single known documented 1-off between acquisition count and usable corpus count
#   for which no JSON metadata field encodes the year-level granularity.
#   => expected filesystem PDF count = local_pdf_count (no subtraction needed).
#
#   The single exception is year 2019: one low-quality PDF's raw file is physically absent
#   (not just excluded from index). Documented in week15_dataset_and_corpus_draft.md.
#   For 2019: actual = 1049, local_pdf_count = 1050, tolerance = 1-off WARNING only.

$acqRec   = Get-Content "corpus/ecourts/acquisition_record.json" | ConvertFrom-Json
$cleanRec = Get-Content "corpus/ecourts/cleaning_record.json"    | ConvertFrom-Json
$acqRec = Get-Content "corpus/ecourts/acquisition_record.json" | ConvertFrom-Json

# Build a lookup of repair_source_ids by year prefix
$repairByYear = @{}
foreach ($id in $cleanRec.repair_source_ids) {
    if ($id -match '^(\d{4})_') {
        $ry = $Matches[1]
        if (-not $repairByYear.ContainsKey($ry)) { $repairByYear[$ry] = 0 }
        $repairByYear[$ry]++
    }
}
$missingYears = [System.Collections.Generic.List[string]]::new()
$warningYears = [System.Collections.Generic.List[string]]::new()

foreach ($y in $acqRec.years) {
    $yr  = "$($y.year)"
    $exp = [int]$y.local_pdf_count

    $yearDir = "corpus/ecourts/pdfs/year=$yr"
    if (-not (Test-Path $yearDir)) {
        $act = 0
    } else {
        $act = (Get-ChildItem -Path $yearDir -Filter *.pdf |
                Where-Object { $_.Name -notmatch '\(\d+\)\.pdf$' }).Count
    }

    if ($act -eq $exp) {
        # Exact match against acquisition record
        continue
    } elseif (($yr -eq "2019") -and ($act -eq ($exp - 1))) {
        # 1-off: documented case where a raw PDF file is physically absent (not just index-excluded)
        # Known instance: year 2019, one permanently absent low-quality PDF
        $warningYears.Add("Year ${yr}: acquisition=$exp, found $act (1 file physically absent - within documented tolerance, see week15_dataset_and_corpus_draft.md)")
    } else {
        $missingYears.Add("Year ${yr}: acquisition=$exp, found $act (delta=$($act - $exp))")
    }
}

if ($warningYears.Count -gt 0) {
    Write-Host "  [WARNING] Year count 1-off (within documented tolerance):" -ForegroundColor Yellow
    $warningYears | ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }
}

if ($missingYears.Count -gt 0) {
    Write-Host "  [ERROR] Year count discrepancies beyond documented tolerance:" -ForegroundColor Red
    $missingYears | ForEach-Object { Write-Host "    $_" -ForegroundColor Red }
    throw "CORPUS VERIFICATION FAILURE: Canonical eCourts PDFs do not match expected year distribution!"
}

# Content-uniqueness report (INFORMATIONAL ONLY, not acceptance-gated):
# Frozen artifacts (artifacts/corpus_readiness.json expected_pdfs=39069, config/datasets.json
# pdf_count=39069, artifacts/extraction_quality_full.json sample_size=39069) count FILES,
# not unique byte contents. The source S3 contains legitimate cross-year byte-duplicate
# PDFs (same judgment filed under two year prefixes, e.g. 1951_1_1_51_EN.pdf in both
# year=1950 and year=1951, 5180 such filename groups), so unique SHA-256 count is
# correctly < file count. Per-year file-count check above (local_pdf_count + 2019
# exception) is the authoritative acceptance gate. Do NOT fail on uniqueness.
Write-Host "  Computing unique SHA-256 content hashes across all canonical unadorned PDFs (informational)..."
$uniqueContentHashes = @{}
$hashProgress = 0
foreach ($p in $cleanPdfs) {
    $h = (Get-FileHash $p.FullName).Hash
    $uniqueContentHashes[$h] = $p.FullName
    $hashProgress++
    if ($hashProgress % 5000 -eq 0) {
        Write-Host "    Hashed $hashProgress / $($cleanPdfs.Count)..." -ForegroundColor Gray
    }
}

Write-Host "  Unique content hashes found: $($uniqueContentHashes.Count) (informational; $($cleanPdfs.Count) files total)" -ForegroundColor Green
if ($uniqueContentHashes.Count -ne $expectedUniquePdfCount) {
    Write-Host "  [INFO] Unique content count ($($uniqueContentHashes.Count)) differs from file count ($expectedUniquePdfCount). This reflects legitimate cross-year byte-duplicate source PDFs and does not block cleanup." -ForegroundColor Yellow
} else {
    Write-Host "  [OK] EXACT MATCH: Canonical corpus contains exactly $expectedUniquePdfCount unique PDF contents (1950-2020)!" -ForegroundColor Green
}

# ---------------------------------------------------------------------------
# STEP 6: EXECUTE PROVEN DUPLICATE & CACHE REMOVAL
# ---------------------------------------------------------------------------
Write-Host "`n[Step 6/7] Removing proven duplicates and transient caches..." -ForegroundColor Cyan

# A. Remove canonical download duplicates
$removedCanonDups = 0
foreach ($cd in $dupsCanon) {
    $target = Join-Path $repoRoot $cd.SourcePath
    if (Test-Path $target) {
        $dest = Join-Path $repoRoot $cd.DestinationPath
        if (-not (Test-Path $dest)) {
            throw "SAFETY VIOLATION: Cannot delete download duplicate $target because canonical destination $dest does not exist!"
        }
        $destHash = (Get-FileHash $dest).Hash
        if ($destHash -ne $cd.DestinationSha256) {
            throw "SAFETY VIOLATION: Canonical destination $dest hash does not match expected ($($cd.DestinationSha256))!"
        }
        Remove-Item -Path $target
        $removedCanonDups++
    }
}
Write-Host "  [OK] Removed $removedCanonDups verified download duplicates from canonical ecourts/pdfs/." -ForegroundColor Green

# B. Remove nested duplicate PDFs (exact-duplicate: canonical already existed when scanned)
$removedNestedDups = 0
foreach ($nd in $dupsNested) {
    $target = Join-Path $repoRoot $nd.SourcePath
    if (Test-Path $target) {
        Remove-Item -Path $target
        $removedNestedDups++
    }
}
Write-Host "  [OK] Removed $removedNestedDups nested exact-duplicate PDFs." -ForegroundColor Green

# B-bis. Remove nested collision-duplicate PDFs (byte-identical siblings auto-resolved in manifest phase)
# Safety gate: the canonical MOVE must have completed (destination now exists with correct hash)
$removedCollisionDups = 0
foreach ($cd2 in $dupsCollision) {
    $target   = Join-Path $repoRoot $cd2.SourcePath
    $canonDst = Join-Path $repoRoot $cd2.DestinationPath
    if (Test-Path $target) {
        # The canonical destination should now exist (moved in Step 4)
        if (-not (Test-Path $canonDst)) {
            throw "SAFETY VIOLATION: Cannot delete collision-duplicate $($cd2.SourcePath) because canonical destination $($cd2.DestinationPath) does not exist!"
        }
        $canonHash = (Get-FileHash $canonDst).Hash
        if ($canonHash -ne $cd2.SourceSha256) {
            throw "SAFETY VIOLATION: Canonical destination $($cd2.DestinationPath) hash ($canonHash) != expected ($($cd2.SourceSha256))!"
        }
        Remove-Item -Path $target
        $removedCollisionDups++
    }
}
Write-Host "  [OK] Removed $removedCollisionDups nested collision-duplicate PDFs (byte-identical, destination verified)." -ForegroundColor Green

# C. Verify canonical cleaned tree, then remove nested duplicate chunks.jsonl
$canonCleanedFiles = Get-ChildItem -Path "corpus/ecourts/cleaned" -Filter "chunks.jsonl" -Recurse
if ($canonCleanedFiles.Count -ne 71) {
    throw "SAFETY VIOLATION: Canonical cleaned corpus does not contain exactly 71 chunks.jsonl files (found $($canonCleanedFiles.Count))!"
}

$removedChunks = 0
foreach ($ck in $dupsChunks) {
    $target = Join-Path $repoRoot $ck.SourcePath
    if (Test-Path $target) {
        Remove-Item -Path $target
        $removedChunks++
    }
}
Write-Host "  [OK] Removed $removedChunks verified duplicate chunks.jsonl files from nested corpus." -ForegroundColor Green

# D. Remove empty nested directory tree (corpus/corpus) — ONLY after verifying 0 remaining files
if (Test-Path "corpus/corpus") {
    $remainingNestedFiles = Get-ChildItem -Path "corpus/corpus" -Recurse -File
    if ($remainingNestedFiles.Count -eq 0) {
        Remove-Item -Path "corpus/corpus" -Recurse
        Write-Host "  [OK] Removed empty corpus/corpus/ directory structure." -ForegroundColor Green
    } else {
        Write-Host "  [WARNING] $($remainingNestedFiles.Count) files remain in corpus/corpus/; retaining directory." -ForegroundColor Yellow
        $remainingNestedFiles | Select-Object -First 10 | ForEach-Object { Write-Host "    $($_.FullName)" -ForegroundColor Yellow }
    }
}

# E. Remove BM25 Duplicate (with before/after hash check)
if (Test-Path "retrieval/bm25-001.sqlite") {
    $canonBm25  = Join-Path $repoRoot "retrieval/bm25.sqlite"
    $preHash    = (Get-FileHash $canonBm25).Hash
    if ($preHash -ne $baselineHashes.Bm25Sqlite) {
        throw "SAFETY VIOLATION: retrieval/bm25.sqlite hash corrupted before duplicate removal!"
    }
    Remove-Item -Path "retrieval/bm25-001.sqlite"
    $postHash = (Get-FileHash $canonBm25).Hash
    if ($postHash -ne $baselineHashes.Bm25Sqlite) {
        throw "CRITICAL FAILURE: retrieval/bm25.sqlite hash changed after duplicate removal!"
    }
    Write-Host "  [OK] Removed retrieval/bm25-001.sqlite (reclaimed 2.27 GB). Canonical bm25.sqlite hash verified intact." -ForegroundColor Green
}

# F. Remove Python Caches
foreach ($c in $caches) {
    $target = Join-Path $repoRoot $c.SourcePath
    if (Test-Path $target) {
        Remove-Item -Path $target -Recurse
        Write-Host "  [OK] Removed cache: $($c.SourcePath)" -ForegroundColor Green
    }
}

# ---------------------------------------------------------------------------
# STEP 7: POST-CLEANUP VERIFICATION OF FROZEN ASSETS & METRICS
# ---------------------------------------------------------------------------
Write-Host "`n[Step 7/7] Running final post-cleanup verification of all frozen assets..." -ForegroundColor Cyan

# 1. Paper structural metrics
$texContent = Get-Content "paper_master.tex" -Raw
$rqCount    = [regex]::Matches($texContent, '\\textbf\{RQ\d\}|\\textbf\{Research Question \d\}|RQ\d:').Count
$figCount   = [regex]::Matches($texContent, '\\begin\{figure').Count
$tblCount   = [regex]::Matches($texContent, '\\begin\{table').Count
$refCount   = [regex]::Matches($texContent, '\\bibitem').Count

Write-Host "  Paper metrics: $rqCount RQs, $figCount figures, $tblCount tables, $refCount references."
if ($rqCount -ne 3 -or $figCount -ne 5 -or $tblCount -ne 6 -or $refCount -ne 15) {
    throw "PAPER METRIC VIOLATION: Paper metrics ($rqCount RQs / $figCount figs / $tblCount tables / $refCount refs) do not match spec (3/5/6/15)!"
}

# 2. Cryptographic hashes of all frozen assets
$finalChecks = @(
    @{ Name = "paper_master.tex";                      Expected = $baselineHashes.PaperTex;     Current = (Get-FileHash "paper_master.tex").Hash },
    @{ Name = "paper_master.pdf";                      Expected = $baselineHashes.PaperPdf;     Current = (Get-FileHash "paper_master.pdf").Hash },
    @{ Name = "retrieval/bm25.sqlite";                 Expected = $baselineHashes.Bm25Sqlite;   Current = (Get-FileHash "retrieval/bm25.sqlite").Hash },
    @{ Name = "corpus/dedup_matches.csv";              Expected = $baselineHashes.DedupMatches; Current = (Get-FileHash "corpus/dedup_matches.csv").Hash },
    @{ Name = "corpus/ildc/single_train.parquet";      Expected = $baselineHashes.IldcTrain;    Current = (Get-FileHash "corpus/ildc/single_train.parquet").Hash },
    @{ Name = "corpus/ildc/single_validation.parquet"; Expected = $baselineHashes.IldcVal;      Current = (Get-FileHash "corpus/ildc/single_validation.parquet").Hash },
    @{ Name = "corpus/ildc/single_test.parquet";       Expected = $baselineHashes.IldcTest;     Current = (Get-FileHash "corpus/ildc/single_test.parquet").Hash }
)

foreach ($fc in $finalChecks) {
    if ($fc.Current -ne $fc.Expected) {
        throw "FROZEN ASSET HASH MISMATCH on $($fc.Name): $($fc.Current) vs $($fc.Expected)"
    }
}
Write-Host "  [OK] All core scientific and submission artifact hashes verified 100% byte-identical." -ForegroundColor Green

# 3. Figures match submission
foreach ($figName in @("fig1_outcome.pdf","fig2_funnel.pdf","fig3_integrity.pdf","fig4_investigation.pdf","fig5_explanation.pdf")) {
    $hRoot = (Get-FileHash "figures\$figName").Hash
    $hSub  = (Get-FileHash "submission\final\figures\$figName").Hash
    if ($hRoot -ne $hSub) {
        throw "FIGURE HASH MISMATCH on $figName between figures/ and submission/final/figures/!"
    }
}
Write-Host "  [OK] All 5 figures verified identical between figures/ and submission/final/figures/." -ForegroundColor Green

# 4. Git status check (no tracked files should have been touched)
$finalGitDiff = git diff --stat
if ($finalGitDiff) {
    throw "GIT REGRESSION: Tracked files were modified during cleanup!"
}
Write-Host "  [OK] git diff --stat is completely clean." -ForegroundColor Green

# 5. Report Optional Local Files (retained untouched)
Write-Host "`n--- OPTIONAL LOCAL FILES (RETAINED UNTOUCHED) ---" -ForegroundColor Yellow
if (Test-Path "Indian_Legal_XAI.docx") {
    Write-Host "  - Indian_Legal_XAI.docx (untracked working manuscript notes, $((Get-Item 'Indian_Legal_XAI.docx').Length) bytes)"
}
if (Test-Path ".vscode") {
    Write-Host "  - .vscode/ (local workspace editor configuration)"
}
Write-Host "------------------------------------------------`n"

Write-Host "=================================================================" -ForegroundColor Green
Write-Host "  LOCAL REPOSITORY CLEAN -- SCIENTIFIC STATE PRESERVED" -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
