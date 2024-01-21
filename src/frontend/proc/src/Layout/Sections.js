import Releases from "../Procedures/Releases";
import TopTeams from "../Procedures/TopTeams";
import Page from "./Page";
import ReleasesByGenre from "../Procedures/ReleasesByGenre";
import ReleasesByCountry from "../Procedures/ReleasesByCountry";
import ReleasesByArtist from "../Procedures/ReleasesByArtist";
import ReleasesByLabel from "../Procedures/ReleasesByLabel";

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
        id: "releases-by-genres",
        label: "Genres",
        content: <ReleasesByGenre/>
    },
        {
        id: "releases-by-country",
        label: "Countries",
        content: <ReleasesByCountry/>
    },
    {
        id: "releases-by-label",
        label: "Labels",
        content: <ReleasesByLabel  />
    },
    {
        id: "artists",
        label: "Artists",
        content: <ReleasesByArtist/>
    }

];

export default Sections;