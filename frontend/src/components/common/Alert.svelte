<script>
	import Snackbar, {Label} from "@smui/snackbar"
	import {alertMessage} from "../../store"

	let alertSnackbar = null

	// Snackbar has a `timeoutMs` param but it has a 4000 min.
	// Also I want to be able to hide the alert as needed (by resetting `alertMessage`).
	$: if ($alertMessage) {
		alertSnackbar.open()
		setTimeout(() => {
			$alertMessage = ""
		}, 4000)
	} else if (alertSnackbar) {
		alertSnackbar.close()
	}
</script>


<Snackbar bind:this={alertSnackbar}>
	<Label>{$alertMessage}</Label>
</Snackbar>


<style>
    :global(.mdc-snackbar) {
        bottom: unset !important;
        top: 0;
    }
</style>