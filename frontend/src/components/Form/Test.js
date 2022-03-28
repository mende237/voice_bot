import React from 'react'
import ReactTree from './Tree'

function Test() {
  const data = [{
    value: 'Parent 1',
    children: [
      {
        value: 'enfant 1',
        children: [
          {
            value: 'enfant 1-1-1',
            children: [
              {
                value: 'enfant 1-1-1-1',
                children: [
                  {
                    value: 'enfant 1-1-1-1-1',
                    children: []
                  },
                  {
                    value: 'enfant 1-1-1-1-2',
                    children: []
                  }
                ]
              }
            ]
          },
          {
            value: 'enfant 1-1-2',
            children: []
          },
          {
            value: 'enfant 1-1-3',
            children: []
          }
        ]
      },
      {
        value: 'enfant 1-2',
        children: []
      },
      {
        value: 'enfant 1-3',
        children: []
      }
    ]
  },
  {
    value: 'Parent 2',
    children: [
      {
        value: 'enfant 2-1',
        children: []
      },
      {
        value: 'enfant 2-2',
        children: []
      },
      {
        value: 'enfant 2-3',
        children: []
      }
    ]
  },
  { value: 'Parent 3', children: [] },
  { value: 'Parent 4', children: [] },
  { value: 'Parent 5', children: [] }
]
  return (
    <div>
      <ReactTree treeData={data}/>
      {console.log(ReactTree)}
    </div>
  )
}

export default Test;