# establishes ssh tunnel to helios.cs.ifmo.ru with port-forwarding. Run only when deployd on Helios

ssh -p 2222 -L 24211:127.0.0.1:24211 s501993@helios.cs.ifmo.ru