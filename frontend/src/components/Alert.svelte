<Snackbar bind:this={alertSnackbar} timeoutMs={4000}>
    <Label>{$alertMessage}</Label>
</Snackbar>

<script>
	import Snackbar, {Label} from "@smui/snackbar"
	import {alertMessage} from "../store"

	let alertSnackbar = null

	$: if ($alertMessage) {
		alertSnackbar.open()
	}
</script>

<style>
    :global(.mdc-snackbar) {
        bottom: unset !important;
        top: 0;
    }
</style>