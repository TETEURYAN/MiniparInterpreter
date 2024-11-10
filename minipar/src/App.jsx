import { Box } from '@chakra-ui/react'
import CodeEditor from './components/ui/code-editor'

function App() {

  return (
    <Box
    minH={'100vh'}
    // display={'flex'}
    // alignItems={'center'}
    // justifyContent={'space-around'}
    color={'white'}
    bg={'#1a202c'}
    px={8}
    py={8}
    >
      <CodeEditor/>
    </Box>
  )
}

export default App
