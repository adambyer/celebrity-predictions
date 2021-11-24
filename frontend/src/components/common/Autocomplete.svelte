<script>
    import {
        createEventDispatcher,
        onMount,
    } from "svelte"
    import Textfield from "@smui/textfield"

    export let searchMethod = () => {}
    export let searchValue = ""

    export function reset() {
        options = []
        searchValue = ""
    }

    onMount(async () => {
        if (searchValue) {
            await search()
            selectOption(options[0])
        }
    })
    
    function searchFocusHandler() {
        searchValue = ""
        options = []
    }

    async function handleSearchInput() {
        if (timer) {
            clearTimeout(timer)
        }

        if (!searchValue) {
            options = []
            return
        }

        timer = setTimeout(async () => (await search()), 300)
    }

    async function search() {
        options = await searchMethod(searchValue)
    }

    function selectOption(option) {
        options = []
        searchValue = option.label
        dispatch("change", option.value)
    }

    const dispatch = createEventDispatcher()
    let options = []
    let timer = null
</script>

<div>
    <Textfield
        bind:value={searchValue}
        label="Search..."
        on:focus={searchFocusHandler}
        on:input={() => handleSearchInput()}
    />
</div>

<div
    class="options"
    class:show={options.length > 0}
>
    {#each options as option}
        <div class="option" on:click={() => selectOption(option)}>{option.label}</div>
    {/each}
</div>

<style lang="scss">
    .options {
        display: none;
        position: absolute;
        z-index: 10;
        border: 1px solid gray;
        padding: 5px;
        background-color: white;
        min-width: 300px;

        &.show {
            display: block;
        }

        .option {
            cursor: pointer;
            background-color: lightgray;
            border-bottom: 1px solid darkgray;
            padding: 5px;

            &:hover {
                background-color: lightblue;
            }
        }
    }
</style>