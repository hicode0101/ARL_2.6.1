from flask_restx import fields, Namespace
from app.utils import get_logger, auth
from . import base_query_fields, ARLResource, get_arl_parser


ns = Namespace('asset_wih', description="资产组 WEB Info Hunter 信息")

logger = get_logger()

base_search_fields = {
    'record_type': fields.String(required=False, description="记录类型"),
    'record_type__neq': fields.String(required=False, description="记录类型不等于（全匹配）"),
    'record_type__not': fields.String(required=False, description="记录类型不包含"),
    'content': fields.String(description="内容"),
    'source': fields.String(description="来源 JS URL"),
    'site': fields.String(description="站点URL"),
    "update_date__dgt": fields.String(description="更新时间大于"),
    "update_date__dlt": fields.String(description="更新时间小于"),
    'scope_id': fields.String(description="范围 ID")
}


base_search_fields.update(base_query_fields)


@ns.route('/')
class ARLAssetWebInfoHunter(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        资产组 WEB Info Hunter 信息查询
        """
        args = self.parser.parse_args()
        data = self.build_data(args=args, collection='asset_wih')

        return data


@ns.route('/export/')
class ARLAssetWIHExport(ARLResource):
    parser = get_arl_parser(base_search_fields, location='args')

    @auth
    @ns.expect(parser)
    def get(self):
        """
        资产分组 WIH 导出
        """
        args = self.parser.parse_args()
        response = self.send_export_file(args=args, _type="asset_wih")

        return response
