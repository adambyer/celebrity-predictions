<script>
    export let metric = null
    export let iconOnly = false
    export let className = ""

    import {
        METRIC_CLASSES,
        METRIC_LABELS_PLURAL,
    } from "../../constants"
</script>

<i class="icon {METRIC_CLASSES[metric]} {className}" title={METRIC_LABELS_PLURAL[metric]}></i>

{#if !iconOnly}
    <span>({METRIC_LABELS_PLURAL[metric]})</span>
{/if}

<style lang="scss">
    .icon {
        padding-right: 15px;
    }
</style>
