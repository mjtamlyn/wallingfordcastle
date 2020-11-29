import React from 'react';
import ReactDOM from 'react-dom';
import Mousetrap from 'mousetrap';
import { disableBodyScroll, clearAllBodyScrollLocks } from 'body-scroll-lock';


// Structure taken from the react docs
// Modified a bit so it looks up the modal root itself, and provides some
// styling.
class Modal extends React.Component {
    constructor(props) {
        super(props);
        this.el = document.createElement('div');
    }

    componentWillMount() {
        this.modalRoot = document.getElementById('modal-container');
    }

    componentDidMount() {
        // The portal element is inserted in the DOM tree after
        // the Modal's children are mounted, meaning that children
        // will be mounted on a detached DOM node. If a child
        // component requires to be attached to the DOM tree
        // immediately when mounted, for example to measure a
        // DOM node, or uses 'autoFocus' in a descendant, add
        // state to Modal and only render the children when Modal
        // is inserted in the DOM tree.
        this.modalRoot.appendChild(this.el);
        Mousetrap.bind('esc', this.props.close);
        disableBodyScroll(this.el);
    }

    componentWillUnmount() {
        this.modalRoot.removeChild(this.el);
        Mousetrap.unbind('esc');
        clearAllBodyScrollLocks();
    }

    render() {
        const modal = (
            <div className={ 'modal ' + this.props.className }>
                <div className="modal__background" onClick={ this.props.close } />
                <div className="modal__content">
                    { this.props.children }
                </div>
            </div>
        );
        return ReactDOM.createPortal(modal, this.el);
    }
}

export default Modal;
