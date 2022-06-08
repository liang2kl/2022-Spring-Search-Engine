import { Box, Table, TableContainer, Tbody, Td, Th, Thead, Tr } from "@chakra-ui/react"
import { useSelector } from "react-redux"
import { selectConfig } from "../slices/searchSlice"

export default function ConfigTable() {
  const config = useSelector(selectConfig)

  const width = config.widthFilter ? 
    `[${config.widthRange[0]}, ${config.widthRange[1]}]` : "unlimited"
  const height = config.heightFilter ?
    `[${config.heightRange[0]}, ${config.heightRange[1]}]` : "unlimited"

  return <TableContainer borderRadius="lg" borderWidth={1} width="100%">
    <Table>
      <Thead>
        <Tr>
          <Th>width</Th>
          <Th>height</Th>
          <Th>limits</Th>
          <Th>color</Th>
        </Tr>
      </Thead>
      <Tbody>
        <Tr>
          <Td>{width}</Td>
          <Td>{height}</Td>
          <Td>{config.limits}</Td>
          <Td >{config.color ?
            <Box backgroundColor={config.color} textColor="transparent">X</Box> : "None"}
          </Td>
        </Tr>

      </Tbody>
    </Table>
  </TableContainer>
}