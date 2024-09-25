export default function VWhitespace({width}) {
    if (!width) width = 1;
    return <div style={{marginBottom: `${width}rem`}}></div>
}
