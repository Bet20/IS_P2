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
import {ApolloClient, InMemoryCache, ApolloProvider, useQuery, gql} from '@apollo/client';
import ReleasesList from "../Components/ReleasesList";

const client = new ApolloClient({
    uri: 'http://0.0.0.0:20003', // Replace with your GraphQL server endpoint
    cache: new InMemoryCache(),
});

const GET_RELEASES_BY_ARTIST = gql`
  query ReleasesByArtist($artistId: Int!) {
    releasesByArtist(artistId: $artistId) {
      id
      title
      status
      year
      genre
      style
      country {
        id
        name
      }
      label {
        id
        name
      }
      artist {
        id
        name
      }
      notes
      created_on
      updated_on
    }
  }
`;

function ReleasesByArtistQL({artistId}) {
    const {loading, error, data} = useQuery(GET_RELEASES_BY_ARTIST, {
        variables: {artistId},
    });

    if (loading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    const releases = data.releasesByArtist;

    // Now you can use the 'releases' data in your component
    console.log(releases);

    return (
        <ReleasesList releases={releases}/>
    );
}


function ReleasesByArtist() {

    const [artists, setArtists] = useState([]);
    const [selectedArtist, setSelectedArtist] = useState({
        id: "",
        artist: ""
    });
    const [releases, setReleases] = useState([]);

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
        fetch('http://localhost:20004/api/artists')
            .then(response => response.json())
            .then(data => {
                setArtists(JSON.parse(data));
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

        if (selectedArtist.id) {
            setTimeout(() => {
                fetch('http://localhost:20004/api/releases_by_artist?artist=' + selectedArtist.id)
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

    }, [selectedArtist])

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
                            value={selectedArtist}
                            label="Country"
                            onChange={(e, v) => {
                                setSelectedArtist(e.target.value)
                            }}
                        >
                            <MenuItem value={""}><em>None</em></MenuItem>
                            {
                                artists && artists.map(c => <MenuItem key={c.id} value={c}>{c.artist}</MenuItem>)
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
                        {selectedArtist ? <CircularProgress/> : "--"}
                    </>
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    selectedArtist ?
                        <ApolloProvider client={client}>
                            <ReleasesByArtist artistId={selectedArtist.id}/>
                        </ApolloProvider>
                        : <CircularProgress/>
                }
            </Container>
        </>
    );
}

export default ReleasesByArtist;
