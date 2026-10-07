<script lang="ts">
    import {getRNG} from "./util";
    import Block from "./Block.svelte";
    import ColorPicker, {A11yVariant} from 'svelte-awesome-color-picker';

    export let cardId: Number;

    let generateOutput = (dict: string[], colNum: number, chunkSize: number): string[][] => {
        if (dict.length === 0) dict = [" "]
        let out = []
        for (let j = 0; j < colNum; j++) {
            let outChunk = []
            for (let k = 0; k < chunkSize; k++) {
                outChunk.push(dict[Math.floor(dict.length * rng())])
            }
            out.push(outChunk)
        }
        return out
    }
    let generateSeed = () => {
        seed = Math.random().toString(36).slice(2, 2 + 16)
    }

    let fileInput: HTMLInputElement;

    let saveConfig = () => {
        const config = {
            version: 1,
            seed,
            input,
            dict,
            customDict,
            exclude,
            cardborder,
            color_choice,
            color_options
        };
        const jsonStr = JSON.stringify(config, null, 2);
        let url: string;
        try {
            const blob = new Blob([jsonStr], { type: "application/json" });
            url = URL.createObjectURL(blob);
        } catch {
            url = "data:application/json;charset=utf-8," + encodeURIComponent(jsonStr);
        }
        const a = document.createElement("a");
        a.href = url;
        const safeSeed = seed.replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 20);
        a.download = `passwordcard-${safeSeed || "config"}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        if (url.startsWith("blob:")) {
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        }
    };

    let triggerLoadFile = () => {
        fileInput?.click();
    };

    let loadConfig = (event: Event) => {
        const target = event.target as HTMLInputElement;
        const file = target.files?.[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const content = e.target?.result as string;
                const data = JSON.parse(content);
                if (typeof data.seed === "string") seed = data.seed;
                if (typeof data.input === "string") input = data.input;
                if (Array.isArray(data.dict)) dict = data.dict;
                if (typeof data.customDict === "string") customDict = data.customDict;
                if (typeof data.exclude === "string") exclude = data.exclude;
                if (typeof data.cardborder === "boolean") cardborder = data.cardborder;
                if (typeof data.color_choice === "number") color_choice = data.color_choice;
                if (Array.isArray(data.color_options)) color_options = data.color_options;
            } catch (err) {
                alert("Failed to load settings: invalid JSON file.");
            }
        };
        reader.readAsText(file);
        target.value = "";
    };

    let classNames = {
        "abcdefghijklmnopqrstuvwxyz": "lowercase latin",
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "uppercase latin",
        "0123456789": "digits",
        ",.;:!?-+*%/&'\"#()": "easy qwertz extra",
        "äöüÄÖÜ": "umlauts",
        ",;.:!?\"\'": "punctuation",
        "([{}])": "parenthesis",
        "+-*/<>=%": "math",
        "|_#~&$§@€": "special"
    }

    let classes = Object.keys(classNames)

    let input = "05ABCDEF16GHIJKL27MNOPQR38STUVWX49YZ?"
    let extraOptions = false;
    let cardborder = true;

    let customDict = ""
    let exclude = ""
    let dict = ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789", ",.;:!?-+*%/&'\"#()"]
    let seed: string = "change me 😀"

    let color_options = [
        {
            fg: [...Array(9)].fill(`#000`),
            bg: [
                "#fff",
                "#d0d0d0",
                "#f6acac",
                "#f6ebac",
                "#c1f6ac",
                "#acf6d6",
                "#acd6f6",
                "#c1acf6",
                "#f6aceb"
            ]
        },
        {
            fg: [...Array(9)].fill(`#000`),
            bg: [
                "#fff",
                '#E6E6FA',
                '#fcaeae',
                '#FFDAB9',
                '#FFFACD',
                '#c8eeb2',
                '#AED8E6',
                '#C8A2C8',
                '#F2C4DE'
            ]
        }
    ]
    $: color_choice = 1;

    $: inputList = Array.from(input)
    $: sortedDict = classes.filter(cls => dict.includes(cls))
    $: fullDict = Array.from(new Set(Array.from(sortedDict.join('') + customDict).filter(c => !exclude.includes(c))))
    let rng: Function;
    let numseed: Number;
    let out: String[][];
    $:{
        rng = getRNG(seed);
        numseed = Math.floor(rng() * 15559) /// used for the colors each block
        out = generateOutput(fullDict, inputList.length, 8);
    }
</script>


<div class="settings">
    <label class="text-label" for={`seed${cardId}`}>seed: <input id={`seed${cardId}`} class="text-input" bind:value={seed}
                                                      placeholder="seed"/>
        <button on:click={generateSeed}>generate</button>
    </label>
    <div class="card-controls">
        <label><input type="checkbox" bind:checked={extraOptions} name="extraOptions"/>options</label>
        <label><input type="checkbox" bind:checked={cardborder} name="cardborder"/>show credit card border <span style="font-size: 7pt">(ISO/IEC 7810 ID-1)</span></label>
        <button on:click={saveConfig} title="Save seed, alphabet, and options to file">save</button>
        <button on:click={triggerLoadFile} title="Load seed, alphabet, and options from file">load</button>
        <input type="file" bind:this={fileInput} on:change={loadConfig} accept=".json,application/json" style="display: none;" />
    </div>
    {#if extraOptions}
        <div class="text-options">
            <label class="text-label" for="input" title="Characters that can be used in the password you remember">input:
                <input id="input" class="text-input" bind:value={input} placeholder="input"/>
            </label>

            <div title="Characters in the resulting password">Output options</div>
            {#each classes as cls}
                <label title="{cls}">
                    <input type="checkbox" bind:group={dict} value={cls}/>
                    {classNames[cls]}
                </label>
            {/each}
            <label class="text-label" for="custom">custom characters:
                <input id="custom" class="text-input" bind:value={customDict} placeholder="custom characters"/>
            </label>
            <label class="text-label" for="excluded">excluded characters:
                <input id="excluded" class="text-input" bind:value={exclude} placeholder="excluded characters"/>
            </label>

        </div>
        <div class="color-options">
            Click to customize colors
            {#each color_options as _,i}
                <div class="color-option">
                    <label>
                        <input type="radio" bind:group={color_choice} value={i}/>

                        {#each Array(9) as _,j}
                        <span class="color-pair">
                            <span class="picker">
                        <ColorPicker
                                components={A11yVariant}
                                bind:hex={color_options[i].fg[j]}
                                --input-size="15px"
                                --picker-height="100px"
                                --picker-width="100px"
                                label=""
                                isAlpha={false}
                                a11yColors={[
		{ bgHex: color_options[i].bg[j], placeholder: '◇' },
	]}
                        />
                            </span>
                            <span class="picker">
                        <ColorPicker
                                components={A11yVariant}
                                bind:hex={color_options[i].bg[j]}
                                --picker-height="100px"
                                --picker-width="100px"
                                label=""
                                isAlpha={false}
                                a11yColors={[
		{ textHex: color_options[i].fg[j], reverse: true, placeholder: '◇' },
	]}
                        />
                                </span></span>
                        {/each}
                    </label>
                </div>
            {/each}

        </div>
    {/if}
</div>
<div class="card">
    <div class:cardborder></div>
    <div class="blocks">
        {#each out as block,i}
            <div class="block-wrapper">
                <Block input={inputList[i]} output={block} colorOffsetIndex={i} seed={numseed}
                       colors={color_options[color_choice]}/>
            </div>
        {/each}
        <div class="block-wrapper" style="width: {39.333 * Math.max(3,8-input.length%8) - 2}px">
            <div class="seedDisplay">{seed}</div>
            <div id="fullDict">{fullDict.join("")}</div>
        </div>
    </div>
</div>


<style>

    .cardborder {
        border: 1px black dashed;
        /*https://en.wikipedia.org/wiki/ISO/IEC_7810*/
        width: 85.6mm;
        height: 53.98mm;
        border-radius: 3mm;
        position: absolute;
        z-index: 0;
    }

    .card {
        width: 85.6mm;
        min-height: 53.98mm;
        /*border-radius: 3mm;*/
        /*border: 1px transparent;*/
        page-break-inside: avoid;
    }


    .blocks {
        display: flex;
        flex-wrap: wrap;
        justify-content: flex-start;
        align-content: flex-start;
        flex-direction: row;
        margin-top: 2px;
        margin-left: 2px;
        padding-top: 3px;
        padding-left: 1px;
        box-sizing: border-box;
        overflow-x: visible;
        z-index: 1;
        position: relative;
    }

    .block-wrapper {
        margin: 1px;
    }

    .text-input {
        width: 100%;
        box-sizing: border-box;
        font-size: 11pt;
        font-family: monospace;
    }

    .text-label {
        font-size: 10pt;
        margin-top: 0.5rem;
        background-color: #d2e8d7;
        border-radius: 2px;
        padding: 2px;
        display: block;
    }


    .settings {
        display: flex;
        flex-direction: column;
    }

    .card-controls {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 0.5rem;
        margin-top: 0.25rem;
    }

    .picker {
        /*border: 1px solid black;*/
        /*border-radius: 5rem;*/
        /*width: fit-content;*/
        margin: 2px;
    }

    .color-pair {
        display: flex;
        flex-direction: column;
        margin: 2px;
        width: 40px;

        border-radius: 0.25rem;

        /* https://codepen.io/lloeki/pen/bGpRzb */
        background-color: #ccc;
        background-size: 10px 10px;
        background-image: linear-gradient( 45deg, #777 25%, transparent 25%, transparent),
        linear-gradient(-45deg, #777 25%, transparent 25%, transparent),
        linear-gradient( 45deg, transparent 75%, #777 75%),
        linear-gradient(-45deg, transparent 75%, #777 75%)
    }

    .color-option > label {
        border-bottom: 1px solid #333;
        display: flex;
        flex-direction: row;
    }

    .color-pair:nth-child(2) {
        /*border-right: 1px solid black;*/
        margin-right: 0.5rem;
    }

    .color-options {
        margin: 0.5rem 0;
    }

    .seedDisplay {
        font-family: monospace;
        font-size: xx-small;
        background-color: grey;
        width: fit-content;
        border-radius: 1px;
        white-space: pre;
    }

    #fullDict {
        width: 100%;
        font-family: monospace;
        font-size: 5pt;
        font-weight: 1;
        overflow-wrap: anywhere;
        word-wrap: anywhere;
        /*hyphens: auto;*/

    }

    @media print {
        .settings {
            display: none !important;
        }

    }
</style>
