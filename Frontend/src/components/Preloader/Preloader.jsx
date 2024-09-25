import {Spinner} from "react-bootstrap";

export default function Preloader(props) {
    let {variant} = props;
    if (variant === undefined || variant === null)
        return <div className="d-flex justify-content-center h-100 w-100 align-items-center">
            <Spinner animation="border" role="status">
                <span className="visually-hidden">Loading...</span>
            </Spinner>
        </div>;
    return <div className="d-flex justify-content-center h-100 w-100 align-items-center">
            <Spinner animation="border" role="status" variant={variant}>
                <span className="visually-hidden">Loading...</span>
            </Spinner>
        </div>;
}
