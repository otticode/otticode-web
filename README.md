# otticode-web

Otticode's web site

## Deployment

```bash
rsync -av --delete --exclude='.git' --exclude='.md' /home/william/ws/otticode/otticode-web/ /var/www/otticode.com/
```
