import {PythonShell} from 'python-shell';
import chalk from "chalk";

let options = {
    mode: 'text',
    pythonOptions: ['-u'], // get print results in real-time
    scriptPath: 'scripts/',
};

let pyshell = new PythonShell('import_spt_features.py', options)
pyshell.on('message', function (message) {
    if (message.indexOf('WARNING') > -1) {
        console.warn(chalk.yellow(message));
    } else if (message.indexOf('INFO: Adding ') > -1) {
        console.log(chalk.green(message))
    } else {
        console.log(message)
    }

})

pyshell.on('stderr', function (stderr) {
    console.error(stderr)
});

// end the input stream and allow the process to exit
pyshell.end(function (err, code, signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
    console.log('The exit signal was: ' + signal);
    console.log('finished');
});
