<script>
    import FormField from "@smui/form-field"
    import Textfield from "@smui/textfield"
    import Select, {Option} from "@smui/select"
    import Checkbox from "@smui/checkbox"
    import Tooltip, {Wrapper} from "@smui/tooltip"
    import Button, {Label} from "@smui/button"

    import Autocomplete from "./common/Autocomplete.svelte"
    import {celebritySearch} from "../autocomplete"

    import {
        alertMessage,
        celebrityTwitterUsername,
    } from "../store"
    import {postRequest} from "../api"
    import {PAGE_USER_PREDICTIONS} from "../constants"
    import {gotoPage} from "../nav"

    async function handleIsEnabledClick(predictionId, isChecked) {
        const data = {
            is_enabled: isChecked,
        }
        const response = await patchRequest(`/user/prediction/${predictionId}`, data)
    }

    async function handleIsAutoDisabledClick(predictionId, isChecked) {
        const data = {
            is_auto_disabled: isChecked,
        }
        const response = await patchRequest(`/user/prediction/${predictionId}`, data)
    }

    async function save() {
        if (isNaN(amount)) {
            $alertMessage = "Invalid Amount"
            return
        }

        const prediction = {
            celebrity_id: celebrityId,
            amount: parseInt(amount),
            metric,
            is_enabled: isEnabled,
            is_auto_disabled: isAutoDisabled,
        }

        try {
            const response = await postRequest("user/prediction", prediction) 
        } catch(error) {
            return
        }

        $alertMessage = "Prediction Saved!"
        reset()
        celebrityAutocomplete.reset()
        gotoPage(PAGE_USER_PREDICTIONS)
    }

    function reset() {
        celebrityId = null
        amount = null
        metric = undefined
        isEnabled = true
        isAutoDisabled = false
    }

    // Binding this to the Autocomplete component so it can be reset.
    // TODO: is there a better way?
    let celebrityAutocomplete = undefined

    let celebrityId = null
    let amount = null
    let metric = undefined  // this will be undefined anyway since it's bound to the Select.
    let isEnabled = true
    let isAutoDisabled = false

    $: isReady = !!(
        celebrityId
        && amount
        && metric
    )

    const metrics = [
        {value: "like", label: "Likes"},
        {value: "tweet", label: "Tweets"},
        {value: "retweet", label: "Retweets"},
        {value: "reply", label: "Replies"},
        {value: "quote", label: "Quotes"},
    ]
</script>

<section>
    <div class="header">
        <h2>New Prediction</h2>
    </div>
    
    <form on:submit|preventDefault={save}>
        <div>
            <Autocomplete
                bind:this={celebrityAutocomplete}
                searchMethod={celebritySearch}
                searchValue={$celebrityTwitterUsername}
                on:change={(event) => celebrityId = event.detail}
            />
        </div>

        <div>
            <Select bind:value={metric} label="What action do you want to predict?">
                {#each metrics as m}
                  <Option value={m.value}>{m.label}</Option>
                {/each}
            </Select>
        </div>

        <div>
            <Textfield bind:value={amount} label="How many do you think will happen?"/>
        </div>

        <div>
            <FormField>
                <span>Enabled</span>
                <Checkbox bind:checked={isEnabled} touch/>
            </FormField>
        </div>

        <div>
            <FormField>
                <span>Automatic Disable</span>

                <Wrapper>
                    <i class="far fa-question-circle"></i>
                    <Tooltip>When checked, this will cause the prediction to be automatically disabled after the next scoring occurs.</Tooltip>
                </Wrapper>

                <Checkbox bind:checked={isAutoDisabled} touch/>
            </FormField>
        </div>

        <div>
            <Button
                variant="raised"
                disabled={!isReady}
            >
                <Label>Save</Label>
            </Button>
        </div>
    </form>
</section>

<style lang="scss">
    :global(.mdc-select, .mdc-text-field) {
        width: 300px;
    }
</style>