<script>
    import Tooltip, {Wrapper} from "@smui/tooltip"
    import Checkbox from "@smui/checkbox"
    import Dialog, {Title, Content, Actions} from "@smui/dialog"
    import Button, {Label as ButtonLabel} from "@smui/button"
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
        Label,
    } from "@smui/data-table"

    import {
        userPredictions,
        userLockedPredictionResults,
        alertMessage,
    } from "../store"
    import {
        patchRequest,
        deleteRequest,
    } from "../api"
    import {gotoPage} from "../nav"
    import {PAGE_CREATE_PREDICTION} from "../constants"
    import {celebrityTitle} from "../celebrity_helpers"

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

    function showTooltip() {
        isToolTipOpen = true
    }

    function hideTooltip() {
        isToolTipOpen = false
    }

    function sorter(a, b) {
        if (a.celebrity.twitter_name > b.celebrity.twitter_name) {
            return 1
        } else if (a.celebrity.twitter_name < b.celebrity.twitter_name) {
            return -1
        }
        return 0
    }

    $: $userPredictions = $userPredictions.sort(sorter)
    $: $userLockedPredictionResults = $userLockedPredictionResults.sort(sorter)

    let isDeleteDialogShown = false
    let deletePredictionId = null
    let isToolTipOpen = false
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
                <ButtonLabel>Cancel</ButtonLabel>
            </Button>
            <Button action="delete">
                <ButtonLabel>Yep, do it.</ButtonLabel>
            </Button>
        </Actions>
    </Dialog>

    <div class="header">
        <h2>Locked Predictions</h2>
        
        <Wrapper>
            <i class="far fa-question-circle"></i>
            <Tooltip>These predictions are locked in and will be scored after all today's ativity has been collected.</Tooltip>
        </Wrapper>
    </div>
    
    <DataTable>
        <Head>
            <Row>
                <Cell>
                    <Label>Who</Label>
                </Cell>
                <Cell>
                    <Label>Action</Label>
                </Cell>
                <Cell>
                    <Label>How Many</Label>
                </Cell>
            </Row>
        </Head>
        <Body>
            {#each $userLockedPredictionResults as predictionResult}
                <Row>
                    <Cell>{celebrityTitle(predictionResult.celebrity)}</Cell>
                    <Cell>{predictionResult.metric}</Cell>
                    <Cell>{predictionResult.amount}</Cell>
                </Row>
            {/each}
        </Body>
    </DataTable>

    <div class="header">
        <h2>Predictions</h2>
        
        <!-- I tried using a Tooltip here but it wouldn't go away when clicked. -->
        <i
            class="fas fa-plus-circle fa-2x add-icon"
            title="Add a Prediction"
            on:click={() => gotoPage(PAGE_CREATE_PREDICTION)}
        ></i>
    </div>
    
    <DataTable>
        <Head>
            <Row>
                <Cell>
                    <Label>Who</Label>
                </Cell>
                <Cell>
                    <Label>Action</Label>
                </Cell>
                <Cell>
                    <Label>Mow Many</Label>
                </Cell>
                <Cell>
                    <Label>Is Enabled</Label>
                </Cell>
                <Cell>
                    <Label>Is Auto Disabled</Label>
                    <Wrapper>
                        <i class="far fa-question-circle"></i>
                        <Tooltip>When checked, this will cause the prediction to be automatically disabled after the next scoring occurs.</Tooltip>
                    </Wrapper>
                </Cell>
                <Cell></Cell>
            </Row>
        </Head>
        <Body>
            {#each $userPredictions as prediction}
                <Row>
                    <Cell>{prediction.celebrity.twitter_name} (@{prediction.celebrity.twitter_username})</Cell>
                    <Cell>{prediction.metric}</Cell>
                    <Cell>{prediction.amount}</Cell>
                    <Cell>
                        <Checkbox
                            bind:checked={prediction.is_enabled}
                            on:change={(event) => handleIsEnabledClick(prediction.id, event.target.checked)}
                        />
                    </Cell>
                    <Cell>
                        <Checkbox
                            bind:checked={prediction.is_auto_disabled}
                            on:change={(event) => handleIsAutoDisabledClick(prediction.id, event.target.checked)}
                        />
                    </Cell>
                    <Cell>
                        <Wrapper>
                            <i class="far fa-trash-alt" on:click={() => showDeleteDialog(prediction.id)}></i>
                            <Tooltip>Delete</Tooltip>
                        </Wrapper>
                    </Cell>
                </Row>
            {/each}
        </Body>
    </DataTable>
</section>

<style lang="scss">
    .header {
        display: flex;
        justify-content: start;
        align-items: center;

        h2 {
            margin-right: 10px
        }
    }

    :global(.mdc-data-table__row--selected) {
        background-color: inherit !important;
    }

    // SMUI has a bug where any checkboxes cause the row selection styling.
    // This is a hack to prevent that so hover styles still work.
    :global(.mdc-data-table__row.mdc-data-table__row--selected) {
        &:hover {
            background-color: rgba(0, 0, 0, 0.04) !important;
        }
    }
</style>