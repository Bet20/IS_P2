import Releases from "../Tables/Releases";
import Artists from "../Tables/Artists";
import Labels from "../Tables/Labels";

const Sections = [

    {
        id: "releases",
        label: "releases",
        content: <Releases/>
    },

    {
        id: "artists",
        label: "Artists",
        content: <Artists/>
    },

    {
        id: "labels",
        label: "Labels",
        content: <Labels/>
    }

];

export default Sections;