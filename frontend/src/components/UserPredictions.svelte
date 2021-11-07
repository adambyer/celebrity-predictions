<script>
    import {userPredictions} from "../store"
    import {patchRequest} from "../api"

    async function handleIsEnabledClick(predictionId, isChecked) {
        console.log("*** handleIsEnabledClick", predictionId, isChecked)
        const data = {
            is_enabled: isChecked,
        }
        const response = await patchRequest(`/user/prediction/${predictionId}`, data)
    }
</script>

<section>
    <h2>Predictions</h2>
    
    <table>
        <thead>
            <tr>
                <th>Twitter Username</th>
                <th>Twitter Name</th>
                <th>Metric</th>
                <th>Amount</th>
                <th>Is Enabled</th>
                <th>Is Auto Disabled</th>
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
                    <input
                        type="checkbox"
                        checked={prediction.is_enabled}
                        on:click|preventDefault={(event) => handleIsEnabledClick(prediction.id, event.target.checked)}
                    />
                </td>
                <td>
                    <input type="checkbox" checked={prediction.is_auto_disabled}/>
                </td>
            </tr>
            {/each}
        </tbody>
    </table>
</section>