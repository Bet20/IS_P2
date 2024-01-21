import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select, Stack} from "@mui/material";
import ReleasesList from "../Components/ReleasesList";

const DEMO_TEAMS = [
    {"team": "Manchester United", country: "UK"},
    {"team": "Manchester City", country: "UK"},
    {"team": "Chelsea", country: "UK"},
    {"team": "Tottenham", country: "UK"},
    {"team": "Fulham", country: "UK"},

    {"team": "Sporting", country: "Portugal"},
    {"team": "Porto", country: "Portugal"},
    {"team": "Benfica", country: "Portugal"},
    {"team": "Braga", country: "Portugal"},

    {"team": "PSG", country: "France"},
    {"team": "Lyon", country: "France"},
    {"team": "Olympique de Marseille", country: "France"}
];

const COUNTRIES = [...new Set(DEMO_TEAMS.map(team => team.country))];


function ReleasesByGenre() {

    const [genres, setGenres] = useState([]);
    const [selectedGenre, setSelectedGenre] = useState("");
    const [releases, setReleases] = useState([]);

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/genres')
            .then(response => response.json())
            .then(data => {
                setGenres(JSON.parse(data).map(d => d.genre));
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

        if (selectedGenre) {
            setTimeout(() => {
                fetch('http://localhost:20004/api/releases_by_genre?genre=' + selectedGenre)
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

    }, [selectedGenre])

    return (
        <>
            <h1>Releases By Genre</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
                        <InputLabel id="countries-select-label">Genre</InputLabel>
                        <Select
                            labelId="countries-select-label"
                            id="demo-simple-select"
                            value={selectedGenre}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedGenre(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                genres && genres.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)
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
                    releases ?
                        <ReleasesList releases={releases}/> : <>
                        {selectedGenre ? <CircularProgress/> : "--"} </>
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        selectedGenre ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default ReleasesByGenre;
