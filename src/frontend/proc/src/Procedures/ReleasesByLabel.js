import React, {useEffect, useState} from "react";
import {
    Box, Card,
    CircularProgress,
    Container,
    FormControl, Grid,
    InputLabel,
    MenuItem,
    Select,
    Stack,
    Item,
    Typography
} from "@mui/material";
import ReleasesList from "../Components/ReleasesList";





function ReleaseByLabel() {

    const [labels, setLabels] = useState([]);
    const [selectedLabel, setSelectedLabel] = useState({
        id: "",
        label: ""
    });
    const [releases, setReleases] = useState([]);

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/labels')
            .then(response => response.json())
            .then(data => {
                setLabels(JSON.parse(data));
                console.log(data)
            })
            .catch(error => {
                console.error('There was an error!', error);
            });
    }, []);

    useEffect(() => {
        //!FIXME: this is to simulate how to retrieve data from the server
        //!FIXME: the entities server URL is available on process.env.REACT_APP_API_ENTITIES_URL
        setProcData(null);
        setGQLData(null);

        if (selectedLabel.id) {
            setTimeout(() => {
                fetch('http://localhost:20004/api/releases_by_label?label=' + selectedLabel.id)
                    .then(response => response.json())
                    .then(data => {
                        setReleases(JSON.parse(data));
                        console.log(data)
                    })
                    .catch(error => {
                        console.error('There was an error!', error);
                    });
            }, 500);
        }

    }, [selectedLabel])

    return (
        <>
            <h1>Top Teams</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Country</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedLabel}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedLabel(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                labels && labels.map(c => <MenuItem key={c.id} value={c}>{c.label}</MenuItem>)
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
                    <>
                    <ReleasesList releases={releases}/>
                        selectedLabel ? <CircularProgress/> : "--"
                    </>
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedLabel ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default ReleaseByLabel;
