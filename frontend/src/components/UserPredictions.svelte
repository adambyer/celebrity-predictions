<script>
    import Tooltip, {Wrapper} from "@smui/tooltip"
    import Checkbox from "@smui/checkbox"
    import Dialog, { Title, Content, Actions } from "@smui/dialog"
    import Button, { Label } from "@smui/button"

    import {
        userPredictions,
        alertMessage,
    } from "../store"
    import {
        patchRequest,
        deleteRequest,
    } from "../api"
    import {gotoPage} from "../nav"
    import {PAGE_CREATE_PREDICTION} from "../constants"

    async function handleIsEnabledClick(predictionId, isChecked) {
        const data = {
            is_enabled: isChecked,
        }
        await patchRequest(`/user/prediction/${predictionId}`, data)
        $alertMessage = "Changes Saved"
    }

    async function handleIsAutoDisabledClick(predictionId, isChecked) {
        const data = {
            is_auto_disabled: isChecked,
        }
        await patchRequest(`/user/prediction/${predictionId}`, data)
        $alertMessage = "Changes Saved"
    }

    function showDeleteDialog(prediction_id) {
        deletePredictionId = prediction_id
        isDeleteDialogShown = true
    }

    async function closeDeleteDialogHandler(event) {
        if (event.detail.action === "delete") {
            await deleteRequest(`/user/prediction/${deletePredictionId}`)
            $userPredictions = $userPredictions.filter(p => p.id !== deletePredictionId)
            deletePredictionId = null
            $alertMessage = "Prediction Deleted"
        }
    }

    let isDeleteDialogShown = false
    let deletePredictionId = null
</script>

<section>
    <Dialog
        bind:open={isDeleteDialogShown}
        on:MDCDialog:closed={closeDeleteDialogHandler}
    >
        <Title>Delete Prediction</Title>
        <Content>
            Are you sure you want to delete this Prediction?
        </Content>
        <Actions>
            <Button action="cancel" default>
                <Label>Cancel</Label>
            </Button>
            <Button action="delete">
                <Label>Yep, do it.</Label>
            </Button>
        </Actions>
    </Dialog>

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
                <th></th>
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
                <td>
                    <Wrapper>
                        <i class="far fa-trash-alt" on:click={() => showDeleteDialog(prediction.id)}></i>
                        <Tooltip>Delete</Tooltip>
                    </Wrapper>
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