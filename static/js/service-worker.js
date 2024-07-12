let startTime = 0;

self.addEventListener('message', function(event) {
    if (event.data.action === 'start') {
        startTime = event.data.startTime;
    } else if (event.data.action === 'stop') {
        const endTime = Date.now();
        const timeSpent = (endTime - startTime) / 1000;
        self.clients.matchAll().then(clients => {
            clients.forEach(client => {
                client.postMessage({ action: 'stop', timeSpent: timeSpent });
            });
        });
    }
});
