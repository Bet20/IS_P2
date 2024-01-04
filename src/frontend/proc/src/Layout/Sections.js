import Releases from "../Procedures/Releases";
import TopTeams from "../Procedures/TopTeams";

const Sections = [
    {
        id: "releases",
        label: "Releases",
        content: <Releases/>
    },
    {
        id: "labels",
        label: "Labels",
        content: "Labels"
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