export default function HWhitespace({width}) {
    if (!width) width = 1;
    return <span style={{marginRight: `${width}rem`}}></span>
}
