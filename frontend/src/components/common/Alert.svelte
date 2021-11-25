<script>
	import Snackbar, {Label} from "@smui/snackbar"
	import {alertMessage} from "../../store"

	let alertSnackbar = null

	$: if ($alertMessage) {
		alertSnackbar.open()
		setTimeout(() => {
			$alertMessage = ""
		}, 4000)
	}
</script>

<Snackbar bind:this={alertSnackbar} timeoutMs={4000}>
    <Label>{$alertMessage}</Label>
</Snackbar>

<style>
    :global(.mdc-snackbar) {
        bottom: unset !important;
        top: 0;
    }
</style>