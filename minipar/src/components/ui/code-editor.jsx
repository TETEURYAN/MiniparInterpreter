import {Box, Button, Heading, HStack, Text} from '@chakra-ui/react'
import Editor from '@monaco-editor/react'
import { useState, useRef } from 'react'
import OutputCode from './output-code';

const CodeEditor = () => {
    const editorRef = useRef();
    const [value, setValue] = useState('');
    const [submit, setSubmit] = useState(false);

    const onMount = (editor) => {
        editorRef.current = editor;
        editor.focus();
    };

    const handleSubmit = () => {
        console.log('Submit');
        setSubmit(true);
    }

    // TODO? ADJUST SYNTAX HIGHLIGHTING https://github.com/tatomyr/estimate-it/blob/master/src/components/Estimate/Editor.js this guy does thit
    return (
        <>
        <Box p={4} borderRadius={10}>
            <HStack spacing={4}>
                <Box w={'50%'} h={'75vh'} bg={'gray.900'} borderRadius={10} p={4} display={'flex'} flexDir={'column'}>
                    <Heading size="md" color={'white'} mb={4}>Minipar Input</Heading>
                    <Editor
                        height="60vh"
                        width="100%"
                        theme="vs-dark"
                        defaultLanguage="minipar"
                        defaultValue=""
                        value={value}
                        onChange={(value) => setValue(value)}
                        options={{ minimap: { enabled: false } }}
                        onMount={onMount}
                    />
                    <Button
                    bg = {'#2c3e50'}
                    color={'white'}
                    onClick={handleSubmit}
                    >
                        Submit
                    </Button>
                </Box>
                <Box w={'50%'} bg={'gray.900'} borderRadius={10} p={4}>
                <OutputCode editorRef={editorRef} submit={setSubmit}/>

                </Box>
            </HStack>
        </Box>
        </>
    )
}
export default CodeEditor;