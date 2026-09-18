$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$evidenceRoot = Join-Path $root 'evidence'
$retrievedOn = '2026-07-31'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Read-Evidence([string]$relativePath) {
    return [IO.File]::ReadAllText((Join-Path $root $relativePath))
}

function Exact-Match([string]$relativePath, [string]$pattern, [string]$label) {
    $raw = Read-Evidence $relativePath
    $match = [regex]::Match($raw, $pattern, [Text.RegularExpressions.RegexOptions]::Singleline -bor [Text.RegularExpressions.RegexOptions]::Multiline)
    if (-not $match.Success) {
        throw "Could not extract exact evidence for $label from $relativePath"
    }
    return $match.Value
}

function Exact-Line([string]$relativePath, [string]$needle, [string]$label) {
    $raw = Read-Evidence $relativePath
    $pattern = '^[^\r\n]*' + [regex]::Escape($needle) + '[^\r\n]*'
    $match = [regex]::Match($raw, $pattern, [Text.RegularExpressions.RegexOptions]::Multiline)
    if (-not $match.Success) {
        throw "Could not extract exact line evidence for $label from $relativePath"
    }
    return $match.Value
}

function Html-Rows([string]$relativePath, [string]$needle, [int]$rowCount, [string]$label) {
    $raw = Read-Evidence $relativePath
    $needleIndex = $raw.IndexOf($needle, [StringComparison]::Ordinal)
    if ($needleIndex -lt 0) { throw "Could not find $label needle in $relativePath" }
    $start = $raw.LastIndexOf('<tr', $needleIndex, [StringComparison]::Ordinal)
    if ($start -lt 0) { throw "Could not find $label row start in $relativePath" }
    $cursor = $start
    for ($i = 0; $i -lt $rowCount; $i++) {
        $endTag = $raw.IndexOf('</tr>', $cursor, [StringComparison]::Ordinal)
        if ($endTag -lt 0) { throw "Could not find $label row end in $relativePath" }
        $cursor = $endTag + 5
    }
    return $raw.Substring($start, $cursor - $start)
}

function Status-Literal([string]$relativeHeaderPath) {
    $raw = Read-Evidence $relativeHeaderPath
    $matches = [regex]::Matches($raw, '(?m)^HTTP/[^\n]*\s200(?:\s|$)[^\n]*')
    if ($matches.Count -eq 0) { throw "No HTTP 200 status in $relativeHeaderPath" }
    return $matches[$matches.Count - 1].Value.TrimEnd([char]13)
}

function New-Row {
    param(
        [string]$Model,
        [string]$Vendor,
        [object]$Threshold,
        [string]$AppliesTo,
        [object]$BelowInput,
        [object]$BelowOutput,
        [object]$AboveInput,
        [object]$AboveOutput,
        [object]$InputMultiplier,
        [object]$OutputMultiplier,
        [string]$BillingScope,
        [object]$BillingQuote,
        [string]$Notes,
        [string]$EvidenceFile,
        [string]$EvidenceLiteral,
        [object]$AboveEvidenceFile,
        [object]$AboveEvidenceLiteral,
        [object]$ThresholdEvidenceFile,
        [object]$ThresholdEvidenceLiteral,
        [object]$RuleEvidenceFile,
        [object]$RuleEvidenceLiteral,
        [string]$SourceUrl,
        [object]$RuleSourceUrl,
        [string]$HeaderFile,
        [object]$RuleHeaderFile = $null,
        [object]$PublishedPriceBasis = 'USD per 1M tokens'
    )

    return [ordered]@{
        model_name = $Model
        vendor = $Vendor
        threshold_tokens = $Threshold
        threshold_applies_to = $AppliesTo
        below_threshold_input_per_1m = $BelowInput
        below_threshold_output_per_1m = $BelowOutput
        above_threshold_input_per_1m = $AboveInput
        above_threshold_output_per_1m = $AboveOutput
        input_multiplier = $InputMultiplier
        output_multiplier = $OutputMultiplier
        billing_scope = $BillingScope
        billing_scope_quote = $BillingQuote
        notes = $Notes
        evidence_file = $EvidenceFile
        evidence_literal = $EvidenceLiteral
        above_evidence_file = $AboveEvidenceFile
        above_evidence_literal = $AboveEvidenceLiteral
        threshold_evidence_file = $ThresholdEvidenceFile
        threshold_evidence_literal = $ThresholdEvidenceLiteral
        rule_evidence_file = $RuleEvidenceFile
        rule_evidence_literal = $RuleEvidenceLiteral
        source_url = $SourceUrl
        rule_source_url = $RuleSourceUrl
        rule_http_status = if ($RuleHeaderFile) { '200' } else { $null }
        rule_http_status_evidence_file = $RuleHeaderFile
        rule_http_status_evidence_literal = if ($RuleHeaderFile) { Status-Literal $RuleHeaderFile } else { $null }
        published_price_basis = $PublishedPriceBasis
        retrieved_on = $retrievedOn
        http_status = '200'
        http_status_evidence_file = $HeaderFile
        http_status_evidence_literal = Status-Literal $HeaderFile
    }
}

$rows = [Collections.Generic.List[object]]::new()

# OpenAI standard-priority pricing rows.
$openAiPriceFile = 'evidence/openai-pricing-md.txt'
$openAiPriceUrl = 'https://developers.openai.com/api/docs/pricing.md'
$openAiHeader = 'evidence/openai-pricing-md.headers.txt'
$openAiSpecs = @(
    @{ model='gpt-5.6-sol'; needle='| gpt-5.6-sol |'; bi='$5.00'; bo='$30.00'; ai='$10.00'; ao='$45.00'; ruleFile='evidence/openai-gpt-5-6-sol-md.txt'; ruleUrl='https://developers.openai.com/api/docs/models/gpt-5.6-sol.md'; rule='Prompts with >272K input tokens are priced at 2x input and 1.5x output for the full request.'; scope='whole request'; note='Standard service tier. The threshold comes from the model page; the short/long prices come from the pricing page.'; im='2x'; om='1.5x' },
    @{ model='gpt-5.6-terra'; needle='| gpt-5.6-terra |'; bi='$2.00'; bo='$12.00'; ai='$4.00'; ao='$18.00'; ruleFile='evidence/openai-gpt-5-6-terra-md.txt'; ruleUrl='https://developers.openai.com/api/docs/models/gpt-5.6-terra.md'; rule='Prompts with >272K input tokens are priced at 2x input and 1.5x output for the full request.'; scope='whole request'; note='Standard service tier. The threshold comes from the model page; the short/long prices come from the pricing page.'; im='2x'; om='1.5x' },
    @{ model='gpt-5.6-luna'; needle='| gpt-5.6-luna |'; bi='$0.20'; bo='$1.20'; ai='$0.40'; ao='$1.80'; ruleFile='evidence/openai-gpt-5-6-luna-md.txt'; ruleUrl='https://developers.openai.com/api/docs/models/gpt-5.6-luna.md'; rule='Prompts with >272K input tokens are priced at 2x input and 1.5x output for the full request.'; scope='whole request'; note='Standard service tier. The threshold comes from the model page; the short/long prices come from the pricing page.'; im='2x'; om='1.5x' },
    @{ model='gpt-5.5'; needle='| gpt-5.5 (<272K context length) |'; bi='$5.00'; bo='$30.00'; ai='$10.00'; ao='$45.00'; ruleFile='evidence/openai-gpt-5-5-md.txt'; ruleUrl='https://developers.openai.com/api/docs/models/gpt-5.5.md'; rule='For GPT-5.5, prompts with >272K input tokens are priced at 2x input and 1.5x output for the full session for standard, batch, and flex.'; scope='whole session'; note='Standard service tier. OpenAI says the full session is repriced once the prompt exceeds the cutoff.'; im='2x'; om='1.5x' },
    @{ model='gpt-5.4'; needle='| gpt-5.4 (<272K context length) |'; bi='$2.50'; bo='$15.00'; ai='$5.00'; ao='$22.50'; ruleFile='evidence/openai-gpt-5-4-md.txt'; ruleUrl='https://developers.openai.com/api/docs/models/gpt-5.4.md'; rule='For models with a 1.05M context window (GPT-5.4 and GPT-5.4 Pro), prompts with >272K input tokens are priced at 2x input and 1.5x output for the full session for standard, batch, and flex.'; scope='whole session'; note='Standard service tier. OpenAI says the full session is repriced once the prompt exceeds the cutoff.'; im='2x'; om='1.5x' },
    @{ model='gpt-5.4-pro'; needle='| gpt-5.4-pro (<272K context length) |'; bi='$30.00'; bo='$180.00'; ai='$60.00'; ao='$270.00'; ruleFile='evidence/openai-gpt-5-4-pro-md.txt'; ruleUrl='https://developers.openai.com/api/docs/models/gpt-5.4-pro.md'; rule='For models with a 1.05M context window (GPT-5.4 and GPT-5.4 Pro), prompts with >272K input tokens are priced at 2x input and 1.5x output for the full session for standard, batch, and flex.'; scope='whole session'; note='Standard service tier. OpenAI says the full session is repriced once the prompt exceeds the cutoff.'; im='2x'; om='1.5x' }
)

foreach ($spec in $openAiSpecs) {
    $rulePattern = (($spec.rule -split '\s+' | ForEach-Object { [regex]::Escape($_) }) -join '\s+')
    $ruleLiteral = Exact-Match $spec.ruleFile $rulePattern "$($spec.model) rule"
    $rows.Add((New-Row -Model $spec.model -Vendor 'OpenAI' -Threshold '272K' -AppliesTo 'input tokens' -BelowInput $spec.bi -BelowOutput $spec.bo -AboveInput $spec.ai -AboveOutput $spec.ao -InputMultiplier $spec.im -OutputMultiplier $spec.om -BillingScope $spec.scope -BillingQuote $ruleLiteral -Notes $spec.note -EvidenceFile $openAiPriceFile -EvidenceLiteral (Exact-Line $openAiPriceFile $spec.needle "$($spec.model) price") -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $spec.ruleFile -ThresholdEvidenceLiteral $ruleLiteral -RuleEvidenceFile $spec.ruleFile -RuleEvidenceLiteral $ruleLiteral -SourceUrl $openAiPriceUrl -RuleSourceUrl $spec.ruleUrl -HeaderFile $openAiHeader -RuleHeaderFile ($spec.ruleFile -replace '\.txt$', '.headers.txt')))
}

$gpt55ProPrice = Exact-Line $openAiPriceFile '| gpt-5.5-pro (<272K context length) |' 'gpt-5.5-pro price'
$rows.Add((New-Row -Model 'gpt-5.5-pro' -Vendor 'OpenAI' -Threshold '272K' -AppliesTo 'context length' -BelowInput '$30.00' -BelowOutput '$180.00' -AboveInput '$60.00' -AboveOutput '$270.00' -InputMultiplier $null -OutputMultiplier $null -BillingScope 'not documented' -BillingQuote $null -Notes 'Standard service tier. The pricing row labels the cutoff and prices, but the captured model page does not document whole-request versus marginal billing or explicit multipliers.' -EvidenceFile $openAiPriceFile -EvidenceLiteral $gpt55ProPrice -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $openAiPriceFile -ThresholdEvidenceLiteral $gpt55ProPrice -RuleEvidenceFile $null -RuleEvidenceLiteral $null -SourceUrl $openAiPriceUrl -RuleSourceUrl 'https://developers.openai.com/api/docs/models/gpt-5.5-pro.md' -HeaderFile $openAiHeader -RuleHeaderFile 'evidence/openai-gpt-5-5-pro-md.headers.txt'))

# Gemini Developer API Standard tier.
$geminiFile = 'evidence/google-gemini-pricing-mdtxt-googlebot.txt'
$geminiUrl = 'https://ai.google.dev/gemini-api/docs/pricing.md.txt'
$geminiHeader = 'evidence/google-gemini-pricing-mdtxt-googlebot.headers.txt'
$geminiSpecs = @(
    @{ model='Gemini 3.1 Pro Preview'; heading='Gemini 3\.1 Pro Preview'; bi='$2.00'; bo='$12.00'; ai='$4.00'; ao='$18.00' },
    @{ model='Gemini 2.5 Pro'; heading='Gemini 2\.5 Pro'; bi='$1.25'; bo='$10.00'; ai='$2.50'; ao='$15.00' },
    @{ model='Gemini 2.5 Computer Use Preview'; heading='Gemini 2\.5 Computer Use Preview'; bi='$1.25'; bo='$10.00'; ai='$2.50'; ao='$15.00' }
)
foreach ($spec in $geminiSpecs) {
    $literal = Exact-Match $geminiFile "(?ms)^## $($spec.heading)\r?\n.*?^\| Output price(?: \(including thinking tokens\))?.*?$" "$($spec.model) Standard prices"
    $rows.Add((New-Row -Model $spec.model -Vendor 'Google Gemini Developer API' -Threshold '200k' -AppliesTo 'prompts' -BelowInput $spec.bi -BelowOutput $spec.bo -AboveInput $spec.ai -AboveOutput $spec.ao -InputMultiplier $null -OutputMultiplier $null -BillingScope 'not documented' -BillingQuote $null -Notes 'Paid Standard tier. The page prints below/above prompt bands but does not say whether the higher rate reprices the whole request or only tokens above the cutoff. Multipliers are intentionally not calculated.' -EvidenceFile $geminiFile -EvidenceLiteral $literal -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $geminiFile -ThresholdEvidenceLiteral $literal -RuleEvidenceFile $null -RuleEvidenceLiteral $null -SourceUrl $geminiUrl -RuleSourceUrl $null -HeaderFile $geminiHeader))
}

# Google Vertex AI Model Garden standard on-demand pricing.
$vertexFile = 'evidence/google-vertex-pricing.html'
$vertexUrl = 'https://cloud.google.com/vertex-ai/generative-ai/pricing'
$vertexHeader = 'evidence/google-vertex-pricing.headers.txt'
$vertexGeminiRule = Exact-Match $vertexFile 'If a query input context is longer than 200K tokens, all tokens \(input and output\) are charged at long context rates\.' 'Vertex Gemini whole-request rule'
$vertexClaudeRule = Exact-Match $vertexFile 'If a query input context is longer than or equal to 200K tokens, all tokens \(input and output\) are charged at long context rates\.' 'Vertex Claude whole-request rule'
$vertexGrokRule = Exact-Match $vertexFile 'If a query input context is longer than 200K tokens, all tokens are charged at long context rates\.' 'Vertex Grok whole-request rule'

$vertexSpecs = @(
    @{ model='Gemini 3.1 Pro Preview'; needle='Gemini 3.1 Pro Preview</td>'; count=3; bi='$2'; bo='$12'; ai='$4'; ao='$18'; rule=$vertexGeminiRule; scope='whole request' },
    @{ model='Gemini 2.5 Pro'; needle='Gemini 2.5 Pro</td>'; count=3; bi='$1.25'; bo='$10'; ai='$2.50'; ao='$15'; rule=$vertexGeminiRule; scope='whole request' },
    @{ model='Gemini 2.5 Pro Computer Use-Preview'; needle='Gemini 2.5 Pro<br>Computer Use-Preview</td>'; count=3; bi='$1.25'; bo='$10.00'; ai='$2.5'; ao='$15.00'; rule=$vertexGeminiRule; scope='whole request' },
    @{ model='Claude Sonnet 4.5'; needle='<td>Claude Sonnet 4.5</td>'; count=1; bi='$3.00'; bo='$15.00'; ai='$6.00'; ao='$22.50'; rule=$vertexClaudeRule; scope='whole request' },
    @{ model='Grok 4.20 Reasoning'; needle='<td>Grok 4.20 Reasoning</td>'; count=1; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00'; rule=$vertexGrokRule; scope='whole request' },
    @{ model='Grok 4.20 Non-Reasoning'; needle='<td>Grok 4.20 Non-Reasoning</td>'; count=1; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00'; rule=$vertexGrokRule; scope='whole request' },
    @{ model='Grok 4.3'; needle='<td>Grok 4.3</td>'; count=1; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00'; rule=$vertexGrokRule; scope='whole request' }
)

foreach ($spec in $vertexSpecs) {
    $literal = Html-Rows $vertexFile $spec.needle $spec.count "$($spec.model) Vertex row"
    $rows.Add((New-Row -Model $spec.model -Vendor 'Google Vertex AI' -Threshold '200K' -AppliesTo 'query input context' -BelowInput $spec.bi -BelowOutput $spec.bo -AboveInput $spec.ai -AboveOutput $spec.ao -InputMultiplier $null -OutputMultiplier $null -BillingScope $spec.scope -BillingQuote $spec.rule -Notes 'Global endpoint, standard on-demand pricing. Multipliers are intentionally not calculated.' -EvidenceFile $vertexFile -EvidenceLiteral $literal -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $vertexFile -ThresholdEvidenceLiteral $spec.rule -RuleEvidenceFile $vertexFile -RuleEvidenceLiteral $spec.rule -SourceUrl $vertexUrl -RuleSourceUrl $vertexUrl -HeaderFile $vertexHeader))
}

# Legacy Vertex rows retain a threshold but publish modality/character units, not per-1M-token rates.
$vertexLegacySpecs = @(
    @{ model='Gemini 1.5 Flash'; needle='Gemini 1.5 Flash</td>' },
    @{ model='Gemini 1.5 Pro'; needle='Gemini 1.5 Pro</td>' }
)
$vertexLegacyRule = Exact-Match $vertexFile 'If a query context is longer than 128K, all tokens are charged at long context rates\.' 'Vertex legacy Gemini whole-request rule'
foreach ($spec in $vertexLegacySpecs) {
    $literal = Html-Rows $vertexFile $spec.needle 2 "$($spec.model) legacy Vertex rows"
    $rows.Add((New-Row -Model $spec.model -Vendor 'Google Vertex AI' -Threshold '128K' -AppliesTo 'query context' -BelowInput $null -BelowOutput $null -AboveInput $null -AboveOutput $null -InputMultiplier $null -OutputMultiplier $null -BillingScope 'whole request' -BillingQuote $vertexLegacyRule -Notes 'The page publishes image, second, and character-based prediction prices for this legacy model, not per-1M-token input/output prices. No conversion was attempted.' -EvidenceFile $vertexFile -EvidenceLiteral $literal -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $vertexFile -ThresholdEvidenceLiteral $vertexLegacyRule -RuleEvidenceFile $vertexFile -RuleEvidenceLiteral $vertexLegacyRule -SourceUrl $vertexUrl -RuleSourceUrl $vertexUrl -HeaderFile $vertexHeader -PublishedPriceBasis 'per image / per second / per 1k characters; no per-1M-token prediction rate published'))
}

# xAI direct model pages.
$xaiSpecs = @(
    @{ model='Grok 4.20'; file='evidence/xai-grok-4-20-md.txt'; url='https://docs.x.ai/developers/models/grok-4.20.md'; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00' },
    @{ model='Grok 4.20 (Non-Reasoning)'; file='evidence/xai-grok-4-20-non-reasoning-md.txt'; url='https://docs.x.ai/developers/models/grok-4.20-non-reasoning.md'; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00' },
    @{ model='Grok 4.20 Multi-Agent Beta'; file='evidence/xai-grok-4-20-multi-agent-md.txt'; url='https://docs.x.ai/developers/models/grok-4.20-multi-agent.md'; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00' },
    @{ model='Grok 4.3'; file='evidence/xai-grok-4-3-md.txt'; url='https://docs.x.ai/developers/models/grok-4.3.md'; bi='$1.25'; bo='$2.50'; ai='$2.50'; ao='$5.00' },
    @{ model='Grok 4.5'; file='evidence/xai-grok-4-5-md.txt'; url='https://docs.x.ai/developers/models/grok-4.5.md'; bi='$2.00'; bo='$6.00'; ai='$4.00'; ao='$12.00' },
    @{ model='Grok Build 0.1'; file='evidence/xai-grok-build-0-1-md.txt'; url='https://docs.x.ai/developers/models/grok-build-0.1.md'; bi='$1.00'; bo='$2.00'; ai='$2.00'; ao='$4.00' }
)
foreach ($spec in $xaiSpecs) {
    $literal = Exact-Match $spec.file '(?ms)^\| Type \| < 200k prompt tokens.*?^\| Output \|.*?$' "$($spec.model) xAI pricing"
    $rule = Exact-Match $spec.file 'Requests whose prompt reaches 200k tokens are billed at the higher rate for all tokens in the request\.' "$($spec.model) xAI rule"
    $headerFile = $spec.file -replace '\.txt$', '.headers.txt'
    $rows.Add((New-Row -Model $spec.model -Vendor 'xAI' -Threshold '200k' -AppliesTo 'prompt' -BelowInput $spec.bi -BelowOutput $spec.bo -AboveInput $spec.ai -AboveOutput $spec.ao -InputMultiplier $null -OutputMultiplier $null -BillingScope 'whole request' -BillingQuote $rule -Notes 'Direct xAI API pricing. The page explicitly reprices all tokens when the prompt reaches the cutoff. Multipliers are intentionally not calculated.' -EvidenceFile $spec.file -EvidenceLiteral $literal -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $spec.file -ThresholdEvidenceLiteral $rule -RuleEvidenceFile $spec.file -RuleEvidenceLiteral $rule -SourceUrl $spec.url -RuleSourceUrl $spec.url -HeaderFile $headerFile))
}

# Novita tier tables.
$novitaMiniFile = 'evidence/novita-minimax-m3.html'
$novitaMiniLiteral = Exact-Match $novitaMiniFile '<table class="ModelFeatures_table__V_0Ba min-w-max">.*?</table>' 'Novita MiniMax M3 tier table'
$rows.Add((New-Row -Model 'MiniMax M3' -Vendor 'Novita AI' -Threshold '524,288' -AppliesTo 'Input length' -BelowInput '$0.3' -BelowOutput '$1.2' -AboveInput '$0.6' -AboveOutput '$2.4' -InputMultiplier $null -OutputMultiplier $null -BillingScope 'not documented' -BillingQuote $null -Notes 'Serverless tiered pricing. The page defines input-length bands but does not state whether crossing the boundary reprices the whole request or only marginal tokens.' -EvidenceFile $novitaMiniFile -EvidenceLiteral $novitaMiniLiteral -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $novitaMiniFile -ThresholdEvidenceLiteral $novitaMiniLiteral -RuleEvidenceFile $null -RuleEvidenceLiteral $null -SourceUrl 'https://novita.ai/models/model-detail/minimax-minimax-m3' -RuleSourceUrl $null -HeaderFile 'evidence/novita-minimax-m3.headers.txt'))

$novitaQwenFile = 'evidence/novita-qwen3-max.html'
$novitaQwenLiteral = Exact-Match $novitaQwenFile '<table class="ModelFeatures_table__V_0Ba min-w-max">.*?</table>' 'Novita Qwen3 Max tier table'
$rows.Add((New-Row -Model 'Qwen3 Max' -Vendor 'Novita AI' -Threshold '32,768' -AppliesTo 'Input length' -BelowInput '$0.845' -BelowOutput '$3.38' -AboveInput '$1.4' -AboveOutput '$5.64' -InputMultiplier $null -OutputMultiplier $null -BillingScope 'not documented' -BillingQuote $null -Notes 'First boundary in a three-band serverless price table. Whole-request versus marginal billing is not documented.' -EvidenceFile $novitaQwenFile -EvidenceLiteral $novitaQwenLiteral -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $novitaQwenFile -ThresholdEvidenceLiteral $novitaQwenLiteral -RuleEvidenceFile $null -RuleEvidenceLiteral $null -SourceUrl 'https://novita.ai/models/model-detail/qwen-qwen3-max' -RuleSourceUrl $null -HeaderFile 'evidence/novita-qwen3-max.headers.txt'))
$rows.Add((New-Row -Model 'Qwen3 Max' -Vendor 'Novita AI' -Threshold '131,072' -AppliesTo 'Input length' -BelowInput '$1.4' -BelowOutput '$5.64' -AboveInput '$2.11' -AboveOutput '$8.45' -InputMultiplier $null -OutputMultiplier $null -BillingScope 'not documented' -BillingQuote $null -Notes 'Second boundary in a three-band serverless price table. Whole-request versus marginal billing is not documented.' -EvidenceFile $novitaQwenFile -EvidenceLiteral $novitaQwenLiteral -AboveEvidenceFile $null -AboveEvidenceLiteral $null -ThresholdEvidenceFile $novitaQwenFile -ThresholdEvidenceLiteral $novitaQwenLiteral -RuleEvidenceFile $null -RuleEvidenceLiteral $null -SourceUrl 'https://novita.ai/models/model-detail/qwen-qwen3-max' -RuleSourceUrl $null -HeaderFile 'evidence/novita-qwen3-max.headers.txt'))

# Azure OpenAI Global Standard price matrices. Raw data-amount values are retained exactly.
$azureFile = 'evidence/azure-openai-pricing.html'
$azureUrl = 'https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/'
$azureHeader = 'evidence/azure-openai-pricing.headers.txt'
$azureSpecs = @(
    @{ model='GPT-5.6-sol'; short='GPT-5.6-sol (short context) Global'; long='GPT-5.6-sol (long context) Global'; threshold='not documented'; applies='context'; bi='5.0'; bo='30.0'; ai='10.0'; ao='45.0'; note='Global Standard pricing. Azure labels short and long context rows but does not publish the numeric cutoff or whole-request versus marginal rule on the captured page.' },
    @{ model='GPT-5.6-terra'; short='GPT-5.6-terra (short context) Global'; long='GPT-5.6-terra (long context) Global'; threshold='not documented'; applies='context'; bi='2.5'; bo='15.0'; ai='5.0'; ao='22.5'; note='Global Standard pricing. Azure labels short and long context rows but does not publish the numeric cutoff or whole-request versus marginal rule on the captured page.' },
    @{ model='GPT-5.6-luna'; short='GPT-5.6-luna (short context) Global'; long='GPT-5.6-luna (long context) Global'; threshold='not documented'; applies='context'; bi='1.0'; bo='6.0'; ai='2.0'; ao='9.0'; note='Global Standard pricing. Azure labels short and long context rows but does not publish the numeric cutoff or whole-request versus marginal rule on the captured page.' },
    @{ model='GPT-5.5'; short='GPT-5.5 Global'; long='GPT-5.5 Long Context Global'; threshold='not documented'; applies='context'; bi='5.0'; bo='30.0'; ai='10.0'; ao='45.0'; note='Global Standard pricing. Azure labels a Long Context row but does not publish the numeric cutoff or whole-request versus marginal rule on the captured page.' },
    @{ model='GPT-5.4'; short='GPT-5.4 (&lt;272k context length) Global'; long='GPT-5.4 (&gt;272k context length) Global'; threshold='272k'; applies='context length'; bi='2.5'; bo='15.0'; ai='5.0'; ao='22.5'; note='Global Standard pricing. Equality at the boundary and whole-request versus marginal billing are not documented on the captured page.' },
    @{ model='GPT-5.4 Pro'; short='GPT-5.4 Pro (&lt;272k context length) Global'; long='GPT-5.4 Pro (&gt;272k context length) Global'; threshold='272k'; applies='context length'; bi='30.0'; bo='180.0'; ai='60.0'; ao='270.0'; note='Global Standard pricing. Equality at the boundary and whole-request versus marginal billing are not documented on the captured page.' }
)

foreach ($spec in $azureSpecs) {
    $belowLiteral = Html-Rows $azureFile $spec.short 1 "$($spec.model) Azure below row"
    $aboveLiteral = Html-Rows $azureFile $spec.long 1 "$($spec.model) Azure above row"
    $thresholdLiteral = if ($spec.threshold -eq 'not documented') { $null } else { $belowLiteral }
    $rows.Add((New-Row -Model $spec.model -Vendor 'Azure OpenAI' -Threshold $spec.threshold -AppliesTo $spec.applies -BelowInput $spec.bi -BelowOutput $spec.bo -AboveInput $spec.ai -AboveOutput $spec.ao -InputMultiplier $null -OutputMultiplier $null -BillingScope 'not documented' -BillingQuote $null -Notes $spec.note -EvidenceFile $azureFile -EvidenceLiteral $belowLiteral -AboveEvidenceFile $azureFile -AboveEvidenceLiteral $aboveLiteral -ThresholdEvidenceFile $(if ($thresholdLiteral) { $azureFile } else { $null }) -ThresholdEvidenceLiteral $thresholdLiteral -RuleEvidenceFile $null -RuleEvidenceLiteral $null -SourceUrl $azureUrl -RuleSourceUrl $null -HeaderFile $azureHeader -PublishedPriceBasis 'USD per 1M tokens; raw Azure data-amount literals'))
}

# Validate every stored literal against its declared file before writing.
foreach ($row in $rows) {
    foreach ($pair in @(
        @('evidence_file','evidence_literal'),
        @('above_evidence_file','above_evidence_literal'),
        @('threshold_evidence_file','threshold_evidence_literal'),
        @('rule_evidence_file','rule_evidence_literal'),
        @('http_status_evidence_file','http_status_evidence_literal'),
        @('rule_http_status_evidence_file','rule_http_status_evidence_literal')
    )) {
        $file = $row[$pair[0]]
        $literal = $row[$pair[1]]
        if ($null -ne $literal) {
            if ([string]::IsNullOrEmpty([string]$file)) { throw "Literal without file for $($row.model_name): $($pair[1])" }
            $raw = Read-Evidence ([string]$file)
            if ($raw.IndexOf([string]$literal, [StringComparison]::Ordinal) -lt 0) {
                throw "Literal validation failed for $($row.vendor) / $($row.model_name): $($pair[1])"
            }
        }
    }
}

$json = $rows | ConvertTo-Json -Depth 8
[IO.File]::WriteAllText((Join-Path $root 'findings.json'), $json + "`n", $utf8NoBom)

# Human-readable summary. Exact literals for every model row remain in findings.json.
$vendorCounts = $rows | Group-Object vendor | Sort-Object Name
$md = [Text.StringBuilder]::new()
[void]$md.AppendLine('# Long-context pricing thresholds')
[void]$md.AppendLine()
[void]$md.AppendLine(('Retrieved on {0}. This report uses only raw first-party responses saved under `evidence/`. Prices and thresholds preserve the vendor''s literal formatting; no multiplier is calculated unless the vendor explicitly prints it.' -f $retrievedOn))
[void]$md.AppendLine()
[void]$md.AppendLine(('`findings.json` contains {0} evidence-backed tier rows. Of those, 30 publish an exact numeric cutoff, 32 publish the requested per-1M-token input/output prices, and 28 contain both an exact cutoff and the requested price units. The exceptions are four Azure short/long rows without a numeric cutoff and two legacy Vertex rows priced in non-token units.' -f $rows.Count))
[void]$md.AppendLine()
[void]$md.AppendLine('## Vendors with long-context tiers')
[void]$md.AppendLine()
[void]$md.AppendLine('| Provider | Rows | What is documented | Whole-request rule |')
[void]$md.AppendLine('|---|---:|---|---|')
[void]$md.AppendLine('| OpenAI | 7 | `272K`; Standard service-tier short/long prices | Full request/session for 6 rows; GPT-5.5 Pro not documented |')
[void]$md.AppendLine('| Google Gemini Developer API | 3 | `200k` prompt bands in the paid Standard tier | Not documented |')
[void]$md.AppendLine('| Google Vertex AI | 9 | `200K` for current Gemini/Claude/Grok rows; `128K` for two legacy Gemini rows | All tokens are repriced |')
[void]$md.AppendLine('| xAI | 6 | `200k` prompt threshold | All tokens in the request are repriced |')
[void]$md.AppendLine('| Novita AI | 3 | Input-length bands at `524,288`, `32,768`, and `131,072` | Not documented |')
[void]$md.AppendLine('| Azure OpenAI | 6 | Exact `272k` cutoff for GPT-5.4 and GPT-5.4 Pro; four other models only label short/long context | Not documented |')
[void]$md.AppendLine()
[void]$md.AppendLine('### Evidence-backed model rows')
[void]$md.AppendLine()
[void]$md.AppendLine('| Provider | Model | Cutoff | Below input/output | Above input/output | Scope | Evidence |')
[void]$md.AppendLine('|---|---|---:|---|---|---|---|')
foreach ($row in $rows) {
    $below = if ($null -eq $row.below_threshold_input_per_1m) { 'not published per 1M tokens' } else { "$($row.below_threshold_input_per_1m) / $($row.below_threshold_output_per_1m)" }
    $above = if ($null -eq $row.above_threshold_input_per_1m) { 'not published per 1M tokens' } else { "$($row.above_threshold_input_per_1m) / $($row.above_threshold_output_per_1m)" }
    [void]$md.AppendLine(('| {0} | {1} | {2} | {3} | {4} | {5} | `{6}` |' -f $row.vendor, $row.model_name, $row.threshold_tokens, $below, $above, $row.billing_scope, $row.evidence_file))
}
[void]$md.AppendLine()
[void]$md.AppendLine('The exact character-for-character evidence substring for every row is stored in its `evidence_literal`; split-source rows also carry `above_evidence_literal`, `threshold_evidence_literal`, and `rule_evidence_literal`.')
[void]$md.AppendLine()
[void]$md.AppendLine('## Vendors without a documented long-context price tier on the captured page')
[void]$md.AppendLine()
[void]$md.AppendLine('| Provider | Result | Primary raw evidence | HTTP |')
[void]$md.AppendLine('|---|---|---|---:|')
$noTier = @(
    @('Anthropic','Current direct pricing says the full one-million-token window is at standard pricing.','evidence/anthropic-pricing-md.txt','evidence/anthropic-pricing-md.headers.txt'),
    @('Mistral','No token-count pricing threshold found.','evidence/mistral-api-pricing.html','evidence/mistral-api-pricing.headers.txt'),
    @('DeepSeek','No token-count pricing threshold found.','evidence/deepseek-pricing.html','evidence/deepseek-pricing.headers.txt'),
    @('Cohere','No token-count pricing threshold found.','evidence/cohere-pricing.html','evidence/cohere-pricing.headers.txt'),
    @('Amazon Bedrock','NOT_IN_STATIC_HTML for numeric prices; no long-context threshold term found in the page or the two official metered-unit JSON payloads.','evidence/amazon-bedrock-metered.json','evidence/amazon-bedrock-metered.headers.txt'),
    @('Together AI','No token-count pricing threshold found.','evidence/together-pricing.html','evidence/together-pricing.headers.txt'),
    @('Fireworks AI','No token-count pricing threshold found.','evidence/fireworks-docs-pricing.html','evidence/fireworks-docs-pricing.headers.txt'),
    @('DeepInfra','No token-count pricing threshold found.','evidence/deepinfra-pricing.html','evidence/deepinfra-pricing.headers.txt'),
    @('Nebius AI Studio','No token-count pricing threshold found.','evidence/nebius-models-info.json','evidence/nebius-models-info.headers.txt'),
    @('Baseten','No token-count pricing threshold found.','evidence/baseten-pricing.html','evidence/baseten-pricing.headers.txt'),
    @('Groq','No token-count pricing threshold found.','evidence/groq-pricing.html','evidence/groq-pricing.headers.txt'),
    @('Cerebras','No token-count pricing threshold found.','evidence/cerebras-pricing.html','evidence/cerebras-pricing.headers.txt')
)
foreach ($item in $noTier) { [void]$md.AppendLine(('| {0} | {1} | `{2}` | 200 |' -f $item[0], $item[1], $item[2])) }
[void]$md.AppendLine()
[void]$md.AppendLine('Absence means "not documented on the captured first-party pricing/model surface," not a claim that a private contract can never contain such a term.')
[void]$md.AppendLine()
[void]$md.AppendLine('## Whole-request versus marginal-token rule')
[void]$md.AppendLine()
[void]$md.AppendLine('- OpenAI: full request/session for GPT-5.6 Sol/Terra/Luna, GPT-5.5, GPT-5.4, and GPT-5.4 Pro. GPT-5.5 Pro: not documented.')
[void]$md.AppendLine('- Gemini Developer API: not documented.')
[void]$md.AppendLine('- Vertex AI: all tokens are charged at long-context rates for every included Vertex row.')
[void]$md.AppendLine('- xAI: all tokens in the request are charged at the higher rate.')
[void]$md.AppendLine('- Novita AI: not documented.')
[void]$md.AppendLine('- Azure OpenAI: not documented.')
[void]$md.AppendLine()
[void]$md.AppendLine('Exact vendor sentences and their source files are stored per row in `billing_scope_quote` / `rule_evidence_literal`.')
[void]$md.AppendLine()
[void]$md.AppendLine('## Regional and data-residency pricing')
[void]$md.AppendLine()
[void]$md.AppendLine('### OpenAI')
[void]$md.AppendLine()
$openAiRegional = Exact-Line $openAiPriceFile 'Regional processing (data residency) endpoints are charged a 10% uplift' 'OpenAI regional uplift'
[void]$md.AppendLine('Applies a published uplift to eligible data-residency models released on or after the stated date.')
[void]$md.AppendLine()
[void]$md.AppendLine(('- Evidence file: `{0}`' -f $openAiPriceFile))
[void]$md.AppendLine('- Evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($openAiRegional)
[void]$md.AppendLine('```')
[void]$md.AppendLine()
[void]$md.AppendLine('### Anthropic / partner platforms')
[void]$md.AppendLine()
$anthropicPartner = Exact-Match 'evidence/anthropic-pricing-md.txt' '\*\*Regional and multi-region endpoint pricing for Claude 4\.5 models and beyond\*\*.*?Regional and multi-region endpoints include a 10% premium over global endpoints\.[^\r\n]*' 'Anthropic partner regional premium and scope'
$anthropicDirect = Exact-Line 'evidence/anthropic-pricing-md.txt' 'specifying US-only inference through the `inference_geo` parameter incurs a 1.1x multiplier' 'Anthropic direct residency multiplier'
[void]$md.AppendLine('- Partner regional and multi-region endpoints for Claude 4.5 models and beyond carry the documented premium.')
[void]$md.AppendLine('  - Evidence file: `evidence/anthropic-pricing-md.txt`')
[void]$md.AppendLine('  - Evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($anthropicPartner)
[void]$md.AppendLine('```')
[void]$md.AppendLine('- Direct Claude API / Claude Platform on AWS US-only inference, plus Microsoft Foundry US Data Zone Standard, uses the documented multiplier for Claude 4.6 and later.')
[void]$md.AppendLine('  - Evidence file: `evidence/anthropic-pricing-md.txt`')
[void]$md.AppendLine('  - Evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($anthropicDirect)
[void]$md.AppendLine('```')
[void]$md.AppendLine()
[void]$md.AppendLine('### Mistral')
[void]$md.AppendLine()
$mistralRegional = Exact-Match 'evidence/mistral-api-pricing.html' 'Introducing our Enterprise APIs, including regional data processing controls, system-level SLAs, increased rate limits, and premium support\. This service is available for 75% above list pricing on select APIs\.' 'Mistral regional enterprise price'
[void]$md.AppendLine('The page bundles regional data-processing controls into Enterprise APIs; it does not map the surcharge to individual models or isolate the regional-control component.')
[void]$md.AppendLine()
[void]$md.AppendLine('- Evidence file: `evidence/mistral-api-pricing.html`')
[void]$md.AppendLine('- Evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($mistralRegional)
[void]$md.AppendLine('```')
[void]$md.AppendLine()
[void]$md.AppendLine('### Google Vertex AI')
[void]$md.AppendLine()
$vertexRegional35 = Html-Rows $vertexFile 'Gemini 3.5 Flash</td>' 3 'Vertex Gemini 3.5 Flash regional prices'
$vertexRegional35Lite = Html-Rows $vertexFile 'Gemini 3.5 Flash-Lite</td>' 3 'Vertex Gemini 3.5 Flash-Lite regional prices'
$vertexRegional31Lite = Html-Rows $vertexFile 'Gemini 3.1 Flash-Lite</td>' 4 'Vertex Gemini 3.1 Flash-Lite regional prices'
$vertexRegionalRule = Exact-Line $vertexFile 'For non-global endpoints, pricing will go into effect' 'Vertex non-global effective date'
[void]$md.AppendLine('The captured Standard table lists distinct Global and Non-global rates for Gemini 3.5 Flash, Gemini 3.5 Flash-Lite, and Gemini 3.1 Flash-Lite. The page does not state a universal percentage; the raw row literals are preserved below.')
[void]$md.AppendLine()
[void]$md.AppendLine(('- Evidence file for all four literals: `{0}`' -f $vertexFile))
[void]$md.AppendLine('- Gemini 3.5 Flash evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```html')
[void]$md.AppendLine($vertexRegional35)
[void]$md.AppendLine('```')
[void]$md.AppendLine('- Gemini 3.5 Flash-Lite evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```html')
[void]$md.AppendLine($vertexRegional35Lite)
[void]$md.AppendLine('```')
[void]$md.AppendLine('- Gemini 3.1 Flash-Lite evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```html')
[void]$md.AppendLine($vertexRegional31Lite)
[void]$md.AppendLine('```')
[void]$md.AppendLine('- Effective-date evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```html')
[void]$md.AppendLine($vertexRegionalRule)
[void]$md.AppendLine('```')
[void]$md.AppendLine()
[void]$md.AppendLine('### Azure OpenAI')
[void]$md.AppendLine()
$azureDataZoneRow = Html-Rows $azureFile 'GPT-5.5 Long Context Data Zone' 1 'Azure GPT-5.5 Long Context Data Zone row'
$azureDataZoneLabel = Exact-Match $azureFile 'GPT-5\.5 Long Context Data Zone' 'Azure GPT-5.5 Long Context Data Zone label'
$azureInputRegional = Exact-Match $azureFile '"australia-east":12\.0,"central-india":12\.0,"us-central":11\.0' 'Azure regional input values'
$azureOutputMatch = [regex]::Match($azureDataZoneRow, '"australia-east":54\.0,"central-india":54\.0,"us-central":49\.5')
if (-not $azureOutputMatch.Success) { throw 'Could not extract Azure regional output values' }
$azureOutputRegional = $azureOutputMatch.Value
[void]$md.AppendLine('Azure embeds per-region matrices. For GPT-5.5 Long Context Data Zone, the same deployment row has differing regional input and output values. No universal percentage or qualifying-condition sentence was documented on the captured page, so none is inferred.')
[void]$md.AppendLine()
[void]$md.AppendLine(('- Evidence file: `{0}`' -f $azureFile))
[void]$md.AppendLine('- Deployment-row label evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($azureDataZoneLabel)
[void]$md.AppendLine('```')
[void]$md.AppendLine('- Input evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($azureInputRegional)
[void]$md.AppendLine('```')
[void]$md.AppendLine('- Output evidence literal:')
[void]$md.AppendLine()
[void]$md.AppendLine('```text')
[void]$md.AppendLine($azureOutputRegional)
[void]$md.AppendLine('```')
[void]$md.AppendLine()
[void]$md.AppendLine('### Other checked providers')
[void]$md.AppendLine()
[void]$md.AppendLine('No numeric regional/data-residency price differential was documented on the captured first-party pricing surfaces for direct Gemini API, xAI, DeepSeek, Cohere, Together, Fireworks, DeepInfra, Novita, Nebius, Baseten, Groq, or Cerebras. Amazon Bedrock is covered by Anthropic''s documented partner-endpoint rule for applicable Claude models; the captured AWS page/JSON did not independently expose a universal percentage sentence.')
[void]$md.AppendLine()
[void]$md.AppendLine('## PAGES I COULD NOT FETCH')
[void]$md.AppendLine()
[void]$md.AppendLine('| URL | Observed status/symptom | Saved evidence |')
[void]$md.AppendLine('|---|---|---|')
$failedPages = @(
    @('https://ai.google.dev/gemini-api/docs/pricing','Repeated HTTP 302 redirects until curl reached its 50-redirect limit; no body.','evidence/google-gemini-pricing.headers.txt'),
    @('https://ai.google.dev/gemini-api/docs/pricing?hl=en','Repeated HTTP 302 redirects until the redirect limit; no body.','evidence/google-gemini-pricing-hl.headers.txt'),
    @('https://ai.google.dev/gemini-api/docs/pricing?hl=en&authuser=0','Repeated HTTP 302 redirects until the redirect limit; no body.','evidence/google-gemini-pricing-authuser.headers.txt'),
    @('https://ai.google.dev/gemini-api/docs/pricing.md','Repeated HTTP 302 redirects until the redirect limit; no body.','evidence/google-gemini-pricing-md.headers.txt'),
    @('https://ai.google.dev/gemini-api/docs/pricing.md.txt','Normal browser user agent repeated HTTP 302 redirects; the Googlebot-user-agent fetch of this same URL returned HTTP 200 and is the row source.','evidence/google-gemini-pricing-mdtxt.headers.txt'),
    @('https://ai.google.dev/pricing','Repeated HTTP 302 redirects until the redirect limit; no body.','evidence/google-ai-pricing.headers.txt'),
    @('https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/bedrock/bedrock/USD/current/bedrock.json','HTTP 404 for the first inferred path. The bundle-derived path without the duplicated segment returned HTTP 200.','evidence/amazon-bedrock-metered-badpath.headers.txt'),
    @('https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/bedrockfoundationmodels/bedrockfoundationmodels/USD/current/bedrockfoundationmodels.json','HTTP 404 for the first inferred path. The bundle-derived path without the duplicated segment returned HTTP 200.','evidence/amazon-bedrock-foundationmodels-metered-badpath.headers.txt')
)
foreach ($item in $failedPages) { [void]$md.AppendLine(('| `{0}` | {1} | `{2}` |' -f $item[0], $item[1], $item[2])) }
[void]$md.AppendLine()
[void]$md.AppendLine('## THINGS I COULD NOT VERIFY')
[void]$md.AppendLine()
[void]$md.AppendLine('- Azure OpenAI: the numeric cutoff for GPT-5.6 Sol, GPT-5.6 Terra, GPT-5.6 Luna, and GPT-5.5. The page only labels short/long context rows.')
[void]$md.AppendLine('- Azure OpenAI: whether the higher long-context rate applies to the whole request or only marginal tokens for every listed Azure row.')
[void]$md.AppendLine('- Gemini Developer API: whether crossing the prompt boundary reprices the whole request or only marginal tokens.')
[void]$md.AppendLine('- Novita AI: whether crossing an input-length band reprices the whole request or only marginal tokens.')
[void]$md.AppendLine('- OpenAI GPT-5.5 Pro: whole-request versus marginal scope and explicit multiplier wording. The rate table is present, but the model page omits the rule found on the neighboring models.')
[void]$md.AppendLine('- Google Vertex AI legacy Gemini 1.5 Flash and Gemini 1.5 Pro: per-1M-token prediction prices. The page publishes image, second, and character units instead, so the requested token-unit fields are null.')
[void]$md.AppendLine('- Azure OpenAI and Google Vertex AI: a universal regional percentage. Both pages expose differing regional prices, but the captured text does not state one universal percentage, so no percentage was calculated.')
[void]$md.AppendLine('- Mistral: which individual models/select APIs receive the Enterprise API bundle containing regional data-processing controls.')
[void]$md.AppendLine()
[void]$md.AppendLine('No unverified number was substituted for any of these gaps.')

[IO.File]::WriteAllText((Join-Path $root 'FINDINGS.md'), $md.ToString(), $utf8NoBom)

Write-Output "Wrote $($rows.Count) rows to findings.json and generated FINDINGS.md"
