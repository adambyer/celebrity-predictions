<script>
    import {
        createEventDispatcher,
        onMount,
    } from "svelte"
    import Textfield from "@smui/textfield"

    export let label = "Search"
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
        label={label}
        on:focus={searchFocusHandler}
        on:input={() => handleSearchInput()}
        variant="outlined"
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
        background-color: rgb(25, 39, 52);
        min-width: 300px;

        &.show {
            display: block;
        }

        .option {
            cursor: pointer;
            padding: 5px;

            &:hover {
                background-color: #263746 !important;
            }
        }
    }
</style>