<script lang="ts">
    import CardGenerator from "./lib/CardGenerator.svelte";


    let cardNum = 1;
</script>

<div class="background">
    <div class="container">
        <div class="settings">
            <h3>Password card</h3>
        </div>
        <div class="cards">
            {#each Array(cardNum) as _,i}
                <div class="card-box">
                    <CardGenerator cardId={i}></CardGenerator>
                </div>
            {/each}
        </div>
        <div class="explanation">
            <button on:click={()=>cardNum++} title="add new card">+</button>
            {#if cardNum > 1}
                <button on:click={()=>cardNum--} title="remove card">-</button>
            {/if}
            <button on:click={()=>window.print()} title="print all cards">print</button>
            <h4>Password Card Generator</h4>
            <p>This tool allows you to generate a card that helps you create and remember secure passwords. It can
                be
                used as an alternative to a password manager or as a way to remember your master password for your
                password manager.</p>
            <h5>Usage</h5>
            <p>To create a new secure password, start by thinking of a password that is easy for you to remember.
                Then,
                come up with a method to convert the characters. For example, you could always choose the yellow and
                top
                left characters. Next, locate each character from your password in the white fields of the card and
                apply the conversion.</p>
            By using this strategy, along with the default seed and settings,
            <pre>password</pre>
            will be transformed into
            <pre>%Z((0'0'Y%OO:6h?</pre>
            .
            This password already has an acceptable entropy score of 84 bits in KeePassXC's generator.

            <h5>Options</h5>
            <p>You can change the seed to modify the characters and colors around each block.</p>
            In the options the character sets for both input (characters that can be used in the password you remember)
            and output (characters in the resulting password) can be changed.
            Seed and output set will be printed in the bottom right corner, so you can recreate the card if
            necessary.
            There are two color sets to choose from but each color can be customized separately as well.
            This way you can even use the same color multiple times (for example if you're color blind).
            To do that just click on the colors in the color customisation option.
            <p>Inspired by <a href="https://github.com/PeterBrockfeld/passwordCardGenerator" target="_blank" rel="noopener noreferrer">PeterBrockfeld/passwordCardGenerator</a>
                and <a href="https://www.ines-it.de/informationssicherheit/passwortkarte/" target="_blank" rel="noopener noreferrer">ines-it password card</a>.
                This implementation is more customizable and supports emoji (not looking pretty).
            </p>
        </div>
    </div>
</div>

<style>

    .background {
        max-width: 100%;
        width: 100vw;
        min-height: 100vh;
        background-color: #5f7a63;
        position: absolute;
        top: 0;
        left: 0;
    }

    .container {
        /*width: 100%;*/
        max-width: 100%;
        background-color: #fff;
        padding: 1rem;
    }

    .explanation {
        margin-top: 0.5rem;
    }

    pre {
        font-family: var(--font-mono, ui-monospace, 'SF Mono', Monaco, Menlo, Consolas, 'Cascadia Mono', 'Roboto Mono', 'DejaVu Sans Mono', monospace);
        font-variant-numeric: slashed-zero tabular-nums;
        font-variant-ligatures: none;
        font-feature-settings: "zero" 1, "tnum" 1, "calt" 0, "liga" 0;
        text-rendering: geometricPrecision;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        white-space: pre;
        margin: 0 -1px;
        border: 1px solid lightgray;
        border-radius: 2px;
        padding: 0 1px;
        display: inline;
    }

    @media (min-width: 600px) {
        .container {
            width: 500px;
            border-radius: 1rem;
            margin: 1rem auto;
        }
    }

    @media (min-width: 1000px) {
        .container {
            width: 900px;
            border-radius: 1rem;
            margin: 1rem auto;
        }
    }

    @media print {
        .settings, .explanation {
            display: none !important;
        }

        .background {
            background-color: #fff;
        }

        .container {
            border-radius: 0;
            padding: 0;
            margin-top: 0;
            margin-left: 0;
            margin-right: 0;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            grid-gap: 2rem;
        }

    }

</style>
