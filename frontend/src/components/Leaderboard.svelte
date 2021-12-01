<script>
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
        Label,
    } from "@smui/data-table"

    import {formatDate} from "../date_helpers"
    import {
        leadersAllTime,
        leadersDaily,
    } from "../store"
</script>

<section>
    <h2>All Time Leaders</h2>

    <DataTable>
        <Body>
            {#each $leadersAllTime as leader, i}
                <Row>
                    <Cell>{i + 1}</Cell>
                    <Cell>{leader["user"]["username"]}</Cell>
                    <Cell>{leader["points"]}</Cell>
                </Row>
            {/each}
        </Body>
    </DataTable>

    <h2>Daily Leaders</h2>

    <DataTable>
        <Body>
            {#each $leadersDaily as leader}
                <Row>
                    <Cell>{formatDate(leader["metric_date"])}</Cell>
                    <Cell>{leader["user"]["username"]}</Cell>
                    <Cell>{leader["points"]}</Cell>
                </Row>
            {/each}
        </Body>
    </DataTable>
</section>
