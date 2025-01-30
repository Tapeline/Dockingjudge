import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeMathjax from 'rehype-mathjax';
import SyntaxHighlighter from "react-syntax-highlighter";
import {atomDark, materialLight} from 'react-syntax-highlighter/dist/esm/styles/prism';
import {Paper, Table, Typography} from "@material-ui/core";
import remarkMath from "remark-math";
import remarkRehype from "remark-rehype";

export default function MarkdownRenderer(props) {
    const {text} = props;

    return (<div className="rendered-md">
        <Markdown remarkPlugins={[remarkGfm, remarkMath, remarkRehype, rehypeMathjax]} components={{
            table(props) {
                const {node, ...rest} = props;
                return <Table {...rest}></Table>
            },
            code: (props) => {
                const {children, className, inline, node, ...rest} = props
                const match = /language-(\w+)/.exec(className || '')
                if (match) console.log(match, children)
                return match ? (
                    <SyntaxHighlighter
                        PreTag={Paper}
                        customStyle={{padding: "1rem"}}
                        language={match[1]}
                        {...props}
                    >{String(children).replace(/\n$/, "")}</SyntaxHighlighter>
                ) : (
                    <code {...rest} className={className}>
                        {children}
                    </code>
                )
            },
            h1(props) {
                const {node, ...rest} = props;
                return <Typography variant="display2" className="dj-beautiful-text" {...rest}></Typography>
            },
            h2(props) {
                const {node, ...rest} = props;
                return <Typography variant="display1" className="dj-beautiful-text" {...rest}></Typography>
            },
            h3(props) {
                const {node, ...rest} = props;
                return <Typography variant="headline" className="dj-beautiful-text" {...rest}></Typography>
            },
            h4(props) {
                const {node, ...rest} = props;
                return <Typography variant="title" className="dj-beautiful-text" {...rest}></Typography>
            },
            p(props) {
                const {node, ...rest} = props;
                return <Typography variant="subheading" className="dj-beautiful-text" {...rest}></Typography>
            },
            blockquote(props) {
                const {node, ...rest} = props;
                return <Paper className="dj-quote" {...rest}></Paper>
            }
        }}>
            {text}
        </Markdown>
    </div>);
}
