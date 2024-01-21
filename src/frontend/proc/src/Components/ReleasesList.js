import {Card, Grid, Stack, Typography} from "@mui/material";
import React from "react";

const ReleasesList = ({ releases }) => {
    return releases ?
                        <Stack gap={1}>
                            {
                                releases.map(data =>
                                    <Card sx={{p: 3}} classname="release-card">
                                        <Grid container spacing={2}>
                                            <Grid item xs={4}>
                                                <Typography variant="h5">{data.title}</Typography>
                                            </Grid>
                                            <Grid item xs={3}>
                                                <Typography>{data.style}</Typography>
                                            </Grid>
                                            <Grid item xs={3}>
                                                <Typography>{data.genre}</Typography>
                                            </Grid>
                                            <Grid item xs={2}>
                                                <Typography style={{fontFamily: 'monospace'}}>{data.year}</Typography>
                                            </Grid>
                                        </Grid>
                                    </Card>
                                )
                            }
                        </Stack> : null
}

export default ReleasesList;