from app.console import main_parser, router
args = main_parser.parse_args()
router.route(args)
