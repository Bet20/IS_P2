import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function Releases() {

    const [selectedDocument, setSelectedDocument] = useState("1");

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
        //!FIXME: this is to simulate how to retrieve data from the server
        //!FIXME: the entities server URL is available on process.env.REACT_APP_API_ENTITIES_URL

        

        setProcData(null);
        setGQLData(null);

        if (selectedDocument) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                fetch(`http://localhost:20004/api/releases`)
                    .then((r) => {
                        if (!r.ok) {
                            throw new Error(`HTTP error! Status: ${r.status}`);
                        }
                        return r.json();
                    })
                    .then((data) => {
                        console.log(data);
                        setProcData(data);
                    })
                    .catch((e) => {
                        console.error("Error fetching data:", e);
                    });
            }, 500);
        
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_GRAPHQL_URL}`);
                // setGQLData(DEMO_TEAMS.filter(t => t.country === selectedCountry));
            }, 1000);
        }
    }, [selectedDocument])

    return (
        <>
            <h1>Releases</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
    <InputLabel id="documents-select-label">Document</InputLabel>
    <Select
        labelId="documents-select-label"
        id="demo-simple-select"
        value={selectedDocument}
        label="Document"
        onChange={(e) => {
            setSelectedDocument(e.target.value)
        }}
    >
        <MenuItem value={""}><em>None</em></MenuItem>
        {
            ['a', 'b', 'c'].map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)
        }
    </Select>
</FormControl>
                </Box>
            </Container>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => <li>{`<b>${data.title}<b>, ${data.genre}, <i>${data.year}</i>`}</li>)
                            }
                        </ul> :
                        selectedDocument ? <CircularProgress/> : "--"
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data}</li>)
                            }
                        </ul> :
                        selectedDocument ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default Releases;
