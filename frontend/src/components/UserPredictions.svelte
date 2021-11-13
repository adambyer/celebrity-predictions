<script>
    import Tooltip, {Wrapper} from "@smui/tooltip"
    import Checkbox from "@smui/checkbox"

    import {userPredictions} from "../store"
    import {patchRequest} from "../api"
    import {gotoPage} from "../nav"
    import {PAGE_CREATE_PREDICTION} from "../constants"

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
</script>

<section>
    <div class="header">
        <h2>Predictions</h2>
        
        <i class="fas fa-plus-circle fa-2x add-icon" on:click={() => gotoPage(PAGE_CREATE_PREDICTION)}></i>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>Twitter Username</th>
                <th>Twitter Name</th>
                <th>Metric</th>
                <th>Amount</th>
                <th>Is Enabled</th>
                <th>
                    <span>Is Auto Disabled</span>
                    <Wrapper>
                        <i class="far fa-question-circle"></i>
                        <Tooltip>When checked, this will cause the prediction to be automatically disabled after the next scoring occurs.</Tooltip>
                    </Wrapper>
                </th>
            </tr>
        </thead>

        <tbody>
            {#each $userPredictions as prediction}
            <tr>
                <td>{prediction.celebrity.twitter_username}</td>
                <td>{prediction.celebrity.twitter_name}</td>
                <td>{prediction.metric}</td>
                <td>{prediction.amount}</td>
                <td>
                    <Checkbox
                        bind:checked={prediction.is_enabled}
                        on:change={(event) => handleIsEnabledClick(prediction.id, event.target.checked)}
                    />
                </td>
                <td>
                    <Checkbox
                        bind:checked={prediction.is_auto_disabled}
                        on:change={(event) => handleIsAutoDisabledClick(prediction.id, event.target.checked)}
                    />
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</section>

<style lang="scss">
    th, td {
        padding: 0 40px 5px 0
    }

    .header {
        display: flex;
        justify-content: start;
        align-items: center;

        h2 {
            margin-right: 10px
        }

        .add-icon {
            cursor: pointer;
            color: blue;

            &:hover {
                color: gray;
            }
        }
    }
</style>