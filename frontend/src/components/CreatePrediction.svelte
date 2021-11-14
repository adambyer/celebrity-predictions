<script>
    import FormField from "@smui/form-field"
    import Textfield from "@smui/textfield"
    import Select, {Option} from "@smui/select"
    import Checkbox from "@smui/checkbox"
    import Tooltip, {Wrapper} from "@smui/tooltip"

    import Autocomplete from "./common/Autocomplete.svelte"
    import {celebritySearch} from "../autocomplete"

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

    let amount = ""
    let metric = ""
    let isEnabled = true
    let isAutoDisabled = false

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
    
    <form>
        <div>
            <Autocomplete
                searchMethod={celebritySearch}
            />
        </div>

        <div>
            <Select bind:value={metric} label="What action do you want to predict?">
                {#each metrics as metric}
                  <Option value={metric.value}>{metric.label}</Option>
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
    </form>
</section>

<style lang="scss">
    :global(.mdc-select, .mdc-text-field) {
        width: 300px;
    }
</style>