<script>
    import DataTable, {
        Head,
        Body,
        Row,
        Cell,
        Label,
    } from "@smui/data-table"

    import {leaders} from "../store"
</script>

<section>
    {#each Object.entries($leaders) as [title, leaderList]}
        <h2>{title}</h2>

        <DataTable>
            <Body>
                {#each leaderList as leader, i}
                    <Row>
                        <Cell>{i + 1}</Cell>
                        <Cell>{leader["user"]["username"]}</Cell>
                        <Cell>{leader["points"]}</Cell>
                    </Row>
                {/each}
            </Body>
        </DataTable>
    {/each}
</section>