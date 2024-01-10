import {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    Stack,
    Button,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow, TextField
} from "@mui/material";

function Labels() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(100000);
    const [newLabel, setNewLabel] = useState("");

    useEffect(() => {
        fetch(`http://0.0.0.0:20001/labels/pageCount`)
            .then((response) => {
                if (response.status === 200) {
                    response.json().then((res) => setMaxDataSize(res));
                }
            }
        )
            .catch((error) => {
                console.error("Fetch Error:", error);
            }
        );
    }, []);

    useEffect(() => {
        setData(null);

            fetch(`http://0.0.0.0:20001/labels/?page=${page}`)
                .then((response) => {
                    if (response.status === 200) {
                        response.json().then((res) => setData(res));
                    }
                })
                .catch((error) => {
                    console.error("Fetch Error:", error);
                });

    }, [page]);

    const handleAddLabel = async () => {
        const [id, name, company_name] = newLabel.split(",");
        if (id !== "" && name !== "" && company_name !== "") {
            try {
                const response = await fetch('http://0.0.0.0:20001/labels', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ id: Number(id), name, company_name})
                });

                if (!response.ok) {
                    throw new Error('Failed to create release');
                }

                setNewLabel("")

            } catch (error) {
                console.error('Error creating release:', error);
            }
        }
    }

    return (
        <>
            <h1>Labels</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell align="left">Name</TableCell>
                            <TableCell align="left">Company Name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            data ?
                                data.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" align="center">{row.id}</TableCell>
                                        <TableCell component="td" scope="row">
                                            {row.name}
                                        </TableCell>

                                        <TableCell component="td" scope="row">
                                            {row.company_name}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }

            <Stack direction="row" sx={{mt: 4}} gap={2}>
            <TextField
                fullWidth
                label="Insert Label, format: (id, name, company_name)"
                value={newLabel}
                onChange={(e) => setNewLabel(e.target.value)}

                variant="filled"
                color="primary"
            />
                <Button
                    variant="contained"
                    onClick={() => handleAddLabel()}
                    >
                    Insert!
                        </Button>
            </Stack>

        </>
    );
}

export default Labels;
