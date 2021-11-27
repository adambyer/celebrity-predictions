<script>
    import Tooltip, {Wrapper} from "@smui/tooltip"
    import Checkbox from "@smui/checkbox"
    import Dialog, {Title, Content, Actions} from "@smui/dialog"
    import Button, {Label as ButtonLabel} from "@smui/button"
    import Textfield from "@smui/textfield"
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
    import {
        PAGE_CREATE_PREDICTION,
        METRIC_CLASSES,
        METRIC_LABELS_PLURAL,
    } from "../constants"
    import CelebrityLink from "./common/CelebrityLink.svelte"
    import MetricLabel from "./common/MetricLabel.svelte"

    function editMode(prediction) {
        editedPrediction = {...prediction}
        setTimeout(() => {
            amountInput.focus()
        }, 100)
    }

    async function exitEditMode() {
        if (!editedPrediction) {
            editedPrediction = null
            return
        }

        const originalPrediction = $userPredictions.find((p) => p.id === editedPrediction.id)

        if (originalPrediction.amount === editedPrediction.amount) {
            editedPrediction = null
            return
        }

        const data = {
            amount: editedPrediction.amount,
        }
        await patchRequest(`/user/prediction/${editedPrediction.id}`, data)
        $alertMessage = "Changes Saved"
        editedPrediction = null
    }

    async function handleAmountKeyUp(event) {
        if (event.keyCode === 13) {
            await exitEditMode()
        }
    }

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

    function sorter(a, b) {
        if (a.celebrity.twitter_name > b.celebrity.twitter_name) {
            return 1
        } else if (a.celebrity.twitter_name < b.celebrity.twitter_name) {
            return -1
        }
        return 0
    }

    let userPredictionsSorted = []
    let userLockedPredictionResultsSorted = []
    let isDeleteDialogShown = false
    let deletePredictionId = null
    let editedPrediction = null
    let amountInput = null

    $: userPredictionsSorted = [...$userPredictions].sort(sorter)
    $: userLockedPredictionResultsSorted = [...$userLockedPredictionResults].sort(sorter)
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
        <h2>Today's Predictions</h2>
        
        <Wrapper>
            <i class="far fa-question-circle fa-lg"></i>
            <Tooltip>
                At the beginning of each day all enabled predictions are copied here and are locked while they await scoring
                which happens at the end of each day after all activity has been collected.
            </Tooltip>
        </Wrapper>
    </div>
    
    <DataTable>
        <Head>
            <Row>
                <Cell>
                    <Label>Who</Label>
                </Cell>
                <Cell>
                    <Label>What</Label>
                </Cell>
                <Cell>
                    <Label>How Many</Label>
                </Cell>
                <Cell>
                    <Label>So Far</Label>
                </Cell>
            </Row>
        </Head>
        <Body>
            {#each userLockedPredictionResultsSorted as p}
                <Row>
                    <Cell>
                        <CelebrityLink celebrity={p.celebrity}/>
                    </Cell>
                    <Cell>
                        <MetricLabel metric={p.metric} iconOnly={true}/>
                    </Cell>
                    <Cell>{p.amount}</Cell>
                    <Cell>{p.current}</Cell>
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
                    <Label>What</Label>
                </Cell>

                <Cell>
                    <Label>Mow Many</Label>
                </Cell>

                <Cell>
                    <Label>Enabled</Label>
                </Cell>

                <Cell>
                    <Label>Auto Disabled</Label>
                    <Wrapper>
                        <i class="far fa-question-circle"></i>
                        <Tooltip>When checked, this will cause the prediction to be automatically disabled after the next scoring occurs.</Tooltip>
                    </Wrapper>
                </Cell>

                <Cell></Cell>
            </Row>
        </Head>
        <Body>
            {#each userPredictionsSorted as p}
                <Row>
                    <Cell>
                        <CelebrityLink celebrity={p.celebrity}/>
                    </Cell>

                    <Cell>
                        <MetricLabel metric={p.metric} iconOnly={true}/>
                    </Cell>

                    <Cell>
                        {#if editedPrediction && editedPrediction.id === p.id}
                            <Textfield
                                bind:value={editedPrediction.amount}
                                bind:this={amountInput}
                                class="amount-input"
                                on:blur={() => exitEditMode()}
                                on:keyup={(event) => handleAmountKeyUp(event)}
                            />
                        {:else}
                            <span on:click={() => editMode(p)}>{p.amount}</span>
                        {/if}
                    </Cell>

                    <Cell>
                        <Checkbox
                            bind:checked={p.is_enabled}
                            on:change={(event) => handleIsEnabledClick(p.id, event.target.checked)}
                        />
                    </Cell>

                    <Cell>
                        <Checkbox
                            bind:checked={p.is_auto_disabled}
                            on:change={(event) => handleIsAutoDisabledClick(p.id, event.target.checked)}
                        />
                    </Cell>

                    <Cell>
                        <Wrapper>
                            <i class="far fa-trash-alt" on:click={() => showDeleteDialog(p.id)}></i>
                            <Tooltip>Delete</Tooltip>
                        </Wrapper>
                    </Cell>
                </Row>
            {/each}
        </Body>
    </DataTable>
</section>

<style lang="scss">
    @import "../css/constants";

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

    :global(.mdc-dialog) {
        background-color: rgba(0, 0, 0, 0.5);

        :global(.mdc-dialog__title) {
            color: black !important;
        }

        :global(.mdc-button__label) {
            color: black !important;
        }
    }

    :global(.mdc-data-table__cell) {
        max-height: 40px;
        
        :global(.amount-input) {
            display: flex;
            align-items: center;
            width: fit-content !important;
            max-height: 40px;

            :global(.mdc-text-field__input) {
                background-color: $primary-white;
                height: fit-content !important;
                max-width: 60px;
                padding: 5px;
                color: black !important;
            }

            :global(.mdc-line-ripple::before), :global(.mdc-line-ripple::after) {
                border-bottom-color: red;
            }
        }
    }
</style>