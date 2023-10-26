def preload(parser):
    # 'safe', 'questionable', 'explicit'
    parser.add_argument('--safety-level', default='safe', choices=['safe', 'questionable', 'explicit'])