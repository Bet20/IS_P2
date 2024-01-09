import React, {useEffect, useState} from "react";
import {Box, CircularProgress, Container, FormControl, InputLabel, MenuItem, Select} from "@mui/material";

function Page({title, config}) {

    const [selectedOption, setSelectedOption] = useState("");
	const [options, setSelectedOptions] = useState([]);

    const [procData, setProcData] = useState(null);
    const [gqlData, setGQLData] = useState(null);

	useEffect(() => {
		if (typeof(config.options) === 'string') {
			fetch(config.options).then(r => r.json()).then(data => {
				setSelectedOptions(data);
			}).catch(e => {
				console.error("Error fetching data:", e);
			});
			return
		}

		setSelectedOptions(config.options);
	}, [])

    useEffect(() => {
        //!FIXME: this is to simulate how to retrieve data from the server
        //!FIXME: the entities server URL is available on process.env.REACT_APP_API_ENTITIES_URL
        setProcData(null);
        setGQLData(null);

        if (selectedOption) {
            setTimeout(() => {
                console.log(`fetching from ${process.env.REACT_APP_API_PROC_URL}`);
                fetch(config.api)
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
        }
    }, [selectedOption])

    return (
        <>
            <h1>{title}</h1>

            <Container maxWidth="100%"
                       sx={{backgroundColor: 'background.default', padding: "2rem", borderRadius: "1rem"}}>
                <Box>
                    <h2 style={{color: "white"}}>Options</h2>
                    <FormControl fullWidth>
    <InputLabel id="documents-select-label">{title}</InputLabel>
    <Select
        labelId="documents-select-label"
        id="demo-simple-select"
        value={selectedOption}
        label={title}
        onChange={(e) => {
            setSelectedOption(e.target.value)
        }}
    >
        <MenuItem value={""}><em>None</em></MenuItem>
        {
            options.length > 0 && options.map(c => <MenuItem key={c} value={c}>{c}</MenuItem>)
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
                                procData.map(data => {
								const k = Object.keys(config.fields)
								let str = ""
								for (let i = 0; i < k.length; i++) {
									if (i > 0) {
										str += ", "
									}
									str += `${data[k[i]]}`
								}
									
								return <li>{str}</li>})
                            }
                        </ul> :
                        selectedOption ? <CircularProgress/> : "--"
                }
                <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data}</li>)
                            }
                        </ul> :
                        selectedOption ? <CircularProgress/> : "--"
                }
            </Container>
        </>
    );
}

export default Page;
