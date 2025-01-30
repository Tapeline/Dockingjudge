import {amber, deepOrange, lightGreen, lime, orange} from "@material-ui/core/colors";

const scoreColors = [
    deepOrange[500],
    orange[500],
    amber[500],
    lime[200],
    lightGreen[400]
]

export function getScoreColor(score) {
    let normScore = score;
    if (normScore < 0) normScore = 0;
    if (normScore > 100) normScore = 100;
    const notch = 100 / scoreColors.length;
    let iBest = 0;
    for (let i = 0; i < scoreColors.length; i++)
        if (Math.abs(notch * i - normScore) < Math.abs(notch * iBest - normScore))
            iBest = i;
    return scoreColors[iBest];
}
