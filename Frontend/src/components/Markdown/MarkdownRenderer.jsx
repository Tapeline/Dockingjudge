import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import SyntaxHighlighter from "react-syntax-highlighter/src/light.js";
import {materialLight} from 'react-syntax-highlighter/dist/esm/styles/prism';
import {Table} from "@material-ui/core";

export default function MarkdownRenderer(props) {
    const {text} = props;

    return (<div className="rendered-md">
        <Markdown remarkPlugins={[remarkGfm]} components={{
            table(props) {
                const {node, ...rest} = props;
                return <Table {...rest}></Table>
            },
            code(props) {
                const {children, className, node, ...rest} = props
                const match = /language-(\w+)/.exec(className || '')
                return match ? (
                    <SyntaxHighlighter
                        {...rest}
                        PreTag="div"
                        children={String(children).replace(/\n$/, '')}
                        language={match[1]}
                        style={materialLight}
                    />
                ) : (
                    <code {...rest} className={className}>
                        {children}
                    </code>
                )
              }
        }}>
            {text}
        </Markdown>
    </div>);
}
