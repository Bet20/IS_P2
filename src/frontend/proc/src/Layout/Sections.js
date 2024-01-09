import Releases from "../Procedures/Releases";
import TopTeams from "../Procedures/TopTeams";
import Page from "./Page";

const Sections = [
    {
        id: "releases",
        label: "Releases",
        content: <Page title="Releases" config={{
            fields: ["title", "genre", "year"],
            options: "0.0.0.0:20004/api/releases_options",
            api: "0.0.0.0:20004/api/releases"
        }}/>
    },
    {
        id: "labels",
        label: "Labels",
        content: <Page title="Labels"  />
    },
    {
        id: "artists",
        label: "Artists",
        content: "Artists"
    },

    {
        id: "top-scorers",
        label: "Top Scorers",
        content: <h1>Top Scorers - Work in progresss</h1>
    }

];

export default Sections;