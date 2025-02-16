const express = require('express');
const os = require('os');
const si = require('systeminformation');

const app = express();
const PORT = 3000;

const getIPAddress = () => {
    const ifaces = os.networkInterfaces();
    const addresses = [];

    for (const iface in ifaces) {
        for (const alias of ifaces[iface]) {
            if (alias.family === 'IPv4' && !alias.internal){
                addresses.push(alias.address);
                return addresses;
            }
        }
    }
}

const getRunningProcesses = () => {
    return new Promise( async (resolve, reject) => {
        
        try {
            const data = await si.processes();
            const processes = data.list.map(proc => ({
                pid: proc.pid,
                tty: proc.tty || 'unknown',
                time: proc.cpu || '0',
                command: proc.command,
            }));
            

            resolve(data);
        } catch (error) {
            reject(error)
        }
    });
}

const getDiskSpace = () => {
    const total = os.totalmem();
    const free = os.freemem();
    return {
        total: total,
        free: free,
        used: total - free,
        percent: ((total - free) / total) * 100,
    }
}

const getUptime = () => {
    return os.uptime();
}

app.get('/', async (req, res) => {
    try {
        const info = {
            'IP Address:': getIPAddress(),
            'Running Processes': await getRunningProcesses(),
            'Disk Space': await getDiskSpace(),
            'Uptime (seconds)': getUptime(),
        };
        res.json(info);
    } catch (error) {
        res.status(500).json({ error: error.message});
    }
});

app.listen(PORT, () => {
    console.log('Service 2 running');
});