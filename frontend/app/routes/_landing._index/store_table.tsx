import {
  useReactTable,
  getCoreRowModel,
  getExpandedRowModel,
  flexRender,
  createColumnHelper,
} from "@tanstack/react-table";
import { ComponentProps, Fragment, ReactNode } from "react";
import { match } from "ts-pattern";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table";
import { Store } from "~/models/store";
import { BookmarkButton } from "./bookmark";
import ExpandButton from "./expand_button";

const helper = createColumnHelper<Store>();

const columns = [
  helper.display({
    id: "expand",
    cell: (props) =>
      props.row.getCanExpand() && (
        <ExpandButton
          key={props.row.getIsExpanded() ? "expanded" : "collapsed"}
          pressed={props.row.getIsExpanded()}
          onPressedChange={props.row.toggleExpanded}
          value={props.row.id}
        />
      ),
  }),
  helper.accessor("brand", {
    header: "廠商",
    cell: (props) =>
      match(props.getValue())
        .with("7-11", () => "7-11")
        .with("FamilyMart", () => "全家")
        .exhaustive(),
  }),
  helper.accessor("name", { header: "店名" }),
  helper.accessor("address", { header: "地址" }),
  helper.accessor("distance", {
    header: "距離",
    cell: (props) => {
      const value = props.getValue();

      if (!value) return null;

      return Intl.NumberFormat("zh-TW", {
        style: "unit",
        unit: "meter",
        maximumFractionDigits: 0,
      }).format(value);
    },
  }),
  helper.display({
    id: "bookmark",
    cell: (props) => <BookmarkButton {...props.row.original} />,
  }),
];

type Props = ComponentProps<typeof Table> & {
  data: Store[];
  expanded?: Store["id"][];
  renderSubComponent?: (data: Store) => ReactNode;
};
function StoreTable({ data, renderSubComponent, expanded, ...props }: Props) {
  const table = useReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getRowId: (row) => row.id,
    getRowCanExpand: () => true,
    state: {
      expanded: expanded?.reduce((acc, id) => {
        return { ...acc, [id]: true };
      }, {} as Record<string, boolean>),
    },
  });

  const head = (
    <TableHeader>
      {table.getHeaderGroups().map((headerGroup) => (
        <TableRow key={headerGroup.id}>
          {headerGroup.headers.map((header) => (
            <TableHead key={header.id} colSpan={header.colSpan}>
              {!header.isPlaceholder &&
                flexRender(header.column.columnDef.header, header.getContext())}
            </TableHead>
          ))}
        </TableRow>
      ))}
    </TableHeader>
  );

  const body = (
    <TableBody>
      {table.getRowModel().rows.map((row) => (
        <Fragment key={row.id}>
          <TableRow>
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </TableCell>
            ))}
          </TableRow>

          {renderSubComponent && row.getIsExpanded() && (
            <TableRow>
              <TableCell colSpan={row.getVisibleCells().length}>
                {renderSubComponent(row.original)}
              </TableCell>
            </TableRow>
          )}
        </Fragment>
      ))}
    </TableBody>
  );

  return (
    <Table {...props}>
      {head}
      {body}
    </Table>
  );
}

export default StoreTable;
