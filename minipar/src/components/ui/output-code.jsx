

import { useState } from 'react';
import { Heading, Text } from '@chakra-ui/react';
import PropTypes from 'prop-types';

const OutputCode = ({ editorRef, output}) => {
    // const [output, setOutput] = useState('')
    // const [submit, setSubmit] = useState(false)
    // if (submit){
    //     runCode();
    // }
    // const runCode = async () => {
    //     const sourceCode = editorRef.current.getValue();
    //     if (sourceCode === '') {
    //         return;
    //     }
    //     try {
    //         console.log('Running code...');
    //         setOutput('Running code...');
    //     } catch (error) {
    //         console.error(error);
            
    //     }
    // }

    
    return (
        <div>
            <Heading size="md" color={'white'} mb={4}>Minipar Output</Heading>
            <Text
                bg={'#27272a'}
                h={'65vh'}
                p={2}
                overflowY="auto"
                whiteSpace="pre-wrap"
            >
                {output ? output : 'Press "Submit" and the output will be displayed here.'}
            </Text>
        </div>
    )
}

OutputCode.propTypes = {
    editorRef: PropTypes.shape({
        current: PropTypes.object
    }).isRequired,
    submit: PropTypes.func.isRequired
};

export default OutputCode;