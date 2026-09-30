param([string]$Manifest = 'output/watermark-removal/inventory.json', [string]$OutputFolder = 'ocr')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType=WindowsRuntime]
$asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function Await-Result($operation, $type) {
    $task = $asTask.MakeGenericMethod($type).Invoke($null, @($operation))
    $task.Wait()
    $task.Result
}
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if (-not $engine) { throw 'No Windows OCR language available.' }
$items = Get-Content -Raw -LiteralPath $Manifest | ConvertFrom-Json
$count = 0
foreach ($item in $items) {
    $outputPath = Join-Path (Split-Path $Manifest) ($OutputFolder + '/' + $item.hash + '.json')
    if (Test-Path -LiteralPath $outputPath) { continue }
    $file = Await-Result ([Windows.Storage.StorageFile]::GetFileFromPathAsync($item.ocrPath)) ([Windows.Storage.StorageFile])
    $stream = Await-Result ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await-Result ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await-Result ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $result = Await-Result ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $lines = @($result.Lines | ForEach-Object {
        @{ text = $_.Text; words = @($_.Words | ForEach-Object { @{ text=$_.Text; x=$_.BoundingRect.X; y=$_.BoundingRect.Y; width=$_.BoundingRect.Width; height=$_.BoundingRect.Height } }) }
    })
    ConvertTo-Json -InputObject $lines -Depth 8 | Set-Content -LiteralPath $outputPath -Encoding UTF8
    $bitmap.Dispose()
    $stream.Dispose()
    $count++
    if ($count % 50 -eq 0) { Write-Output "OCR processed $count images" }
}
Write-Output "OCR finished: $count images"
