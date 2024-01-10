import {useEffect, useState} from "react";
import {
    Button,
    CircularProgress,
    Pagination,
    Paper, Stack,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow, TextField
} from "@mui/material";

const DEMO_PLAYERS = [
    {"id": "31", "name": "Alexis Sanchez", "age": "33"},
    {"id": "39", "name": "Ander Herrera", "age": "33"},
    {"id": "45", "name": "Andreas Pereira", "age": "26"},
    {"id": "51", "name": "Angel Gomes", "age": "22"},
    {"id": "56", "name": "Anthony Martial", "age": "26"},
    {"id": "59", "name": "Antonio Valencia", "age": "37"},
    {"id": "66", "name": "Ashley Young", "age": "37"},
    {"id": "111", "name": "Chris Smalling", "age": "32"},
    {"id": "145", "name": "David de Gea", "age": "31"},
    {"id": "174", "name": "Eric Bertrand Bailly", "age": "28"},
    {"id": "185", "name": "Faustino Marcos Alberto Rojo", "age": "32"},
    {"id": "198", "name": "Frederico Rodrigues Santos", "age": "29"},
    {"id": "241", "name": "James Garner", "age": "21"},
    {"id": "265", "name": "Jesse Lingard", "age": "29"},
    {"id": "293", "name": "José Diogo Dalot Teixeira", "age": "23"},
    {"id": "304", "name": "Juan Mata", "age": "34"},
    {"id": "336", "name": "Lee Grant", "age": "39"},
    {"id": "356", "name": "Luke Shaw", "age": "27"},
    {"id": "368", "name": "Marcus Rashford", "age": "24"},
    {"id": "374", "name": "Marouane Fellaini", "age": "34"},
    {"id": "378", "name": "Mason Greenwood", "age": "20"},
    {"id": "388", "name": "Matteo Darmian", "age": "32"},
    {"id": "426", "name": "Nemanja Matić", "age": "34"},
    {"id": "441", "name": "Paul Pogba", "age": "29"},
    {"id": "449", "name": "Phil Jones", "age": "30"},
    {"id": "472", "name": "Romelu Lukaku", "age": "29"},
    {"id": "495", "name": "Scott McTominay", "age": "25"},
    {"id": "503", "name": "Sergio Germán Romero", "age": "35"},
    {"id": "525", "name": "Tahith Chong", "age": "22"},
    {"id": "546", "name": "Victor Nilsson Lindelöf", "age": "28"}
];


function Releases() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [data, setData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(100000);
    const [newRelease, setNewRelease] = useState("");

    useEffect(() => {
        fetch(`http://0.0.0.0:20001/releases/pageCount`)
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

            fetch(`http://0.0.0.0:20001/releases/?page=${page}`)
                .then((response) => {
                    if (response.status === 200) {
                        response.json().then((res) => setData(res));
                    }
                })
                .catch((error) => {
                    console.error("Fetch Error:", error);
                });

    }, [page]);

    const handleAddRelease = async () => {
        const [id, title, genre, style, year, artist_id, label_id, country] = newRelease.split(",");
        if (id !== "" && title !== "" && genre !== "" && style !== "" && year !== "" && artist_id !== "" && label_id !== "" && country !== "") {
            try {
                const response = await fetch('http://0.0.0.0:20001/releases', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: Number(id),
                        title,
                        genre,
                        style,
                        year,
                        artist_id: Number(artist_id),
                        label_id: Number(label_id),
                        country: Number(country)
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to create release');
                }

                setNewRelease("")

            } catch (error) {
                console.error('Error creating release:', error);
            }
        }
    }

    return (
        <>
            <h1>Releases (<i>total ~= {maxDataSize*PAGE_SIZE}</i>)</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell component="th" width={"1px"} align="center">ID</TableCell>
                            <TableCell>Release Title</TableCell>
                            <TableCell align="center">Genre</TableCell>
                            <TableCell align="center">Style</TableCell>
                            <TableCell align="right">Year</TableCell>
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
                                            {row.title}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.genre}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.style}
                                        </TableCell>
                                        <TableCell component="td" align="center" scope="row">
                                            {row.year}
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
                label="Insert Label, format: (id, title, genre, style, year, artist_id, label_id, country)"
                value={newRelease}
                onChange={(e) => setNewRelease(e.target.value)}

                variant="filled"
                color="primary"
            />
                <Button
                    variant="contained"
                    onClick={() => handleAddRelease()}
                    >
                    Insert!
                        </Button>
            </Stack>

        </>
    );
}

export default Releases;
