Add-Type -AssemblyName System.Speech

$outDir = "C:\kontitemp\ai\circle_the_square\audio-refs"
if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$samples = @{
    "jan_sample.wav" = "Great. Make it so. GET OUT NOW YOU STUPID COW! JUST GET THAT DAMN MEETING ORGANISED!"
    "christina_sample.wav" = "Well every two weeks on a Friday we do a breakfast meeting and offer some pastries loaded with as much sugar as humanly possible."
    "sharon_sample.wav" = "Well I have needs too Jan that must be met."
    "chris_sample.wav" = "You are dreaming Jan. Inception is the name of a film about dreams Jan."
    "rick_sample.wav" = "No relax, he will be out for a while. I think we need the police here."
}

foreach ($item in $samples.GetEnumerator()) {
    $filePath = Join-Path $outDir $item.Name
    $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
    $synth.SetOutputToWaveFile($filePath)
    $synth.Speak($item.Value)
    $synth.Dispose()
    Write-Host "Generated audio: $filePath"
}
