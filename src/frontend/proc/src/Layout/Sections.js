import ReleasesByGenre from "../Procedures/ReleasesByGenre";
import ReleasesByCountry from "../Procedures/ReleasesByCountry";
import ReleasesByArtist from "../Procedures/ReleasesByArtist";
import ReleasesByLabel from "../Procedures/ReleasesByLabel";

const Sections = [
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