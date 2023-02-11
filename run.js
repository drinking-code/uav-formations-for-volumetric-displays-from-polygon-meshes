const child_process = require('child_process')
const path = require('path')
const fs = require('fs')

const pythonBin = path.resolve('venv', 'bin', 'python')
const pythonEntry = path.resolve('main.py')
const mesh = fs.readFileSync('cube.stl', 'utf-8')
// const mesh = fs.readFileSync('monkey.stl', 'utf-8')
const scriptOptions = JSON.stringify({
    max_amount: 500,
    min_distance: .1,
    sharpness_threshold: 160,
    features_only: false,
})
child_process.spawn(pythonBin, [pythonEntry, mesh, scriptOptions], {stdio: 'inherit'})
